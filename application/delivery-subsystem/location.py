import math
import os
import threading
import time
from datetime import datetime
from flask import Blueprint, jsonify, request
from influxdb_client import Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from db import driver, redis_client, influx_client, influx_bucket, influx_org

location_bp = Blueprint('location', __name__)

write_api = influx_client.write_api(write_options=SYNCHRONOUS)
active_threads = {}

STEP = 0.0008


@location_bp.route("/current_position", methods=["GET"])
def current_position():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
    data = redis_client.hgetall(f"pos:{user_id}")
    if not data:
        return jsonify(None), 200
    keys = ["lat", "lon", "delivery_id", "delivery_status", "vehicle_id", "last_seen"]
    return jsonify({k: data.get(k) for k in keys}), 200


@location_bp.route("/set_position", methods=["POST"])
def set_position():
    data = request.get_json() or {}
    user_id = request.args.get('user_id')
    mapping = {
        "user_id": user_id,
        "lat": data.get("lat", 0.0),
        "lon": data.get("lon", 0.0),
        "last_seen": datetime.utcnow().isoformat() + "Z",
    }
    for key in ["delivery_id", "vehicle_id"]:
        if data.get(key) is not None:
            mapping[key] = data[key]
    redis_client.hset(f"pos:{user_id}", mapping=mapping)
    return jsonify({"status": "position updated"}), 200


def get_target(delivery_id, status):
    if not delivery_id:
        return None
    with driver.session() as session:
        record = session.run("MATCH (d:Delivery {id: $id}) RETURN d", id=delivery_id).single()
    if not record:
        return None
    d = record["d"]
    if status == "accepted" and d.get("restaurant_lat") is not None:
        return float(d["restaurant_lat"]), float(d["restaurant_lon"])
    if status in ("in transit", "in_transit") and d.get("customer_lat") is not None:
        return float(d["customer_lat"]), float(d["customer_lon"])
    return None


def move_towards(lat, lon, target):
    d_lat, d_lon = target[0] - lat, target[1] - lon
    distance = math.sqrt(d_lat ** 2 + d_lon ** 2)
    if distance <= 0.0001:
        return lat, lon
    if distance <= STEP:
        return target
    return lat + d_lat / distance * STEP, lon + d_lon / distance * STEP


def tracking_loop(user_id):
    while redis_client.get(f"tracking:{user_id}") == "true":
        data = redis_client.hgetall(f"pos:{user_id}")
        if not data:
            time.sleep(1)
            continue
        lat, lon = float(data.get("lat", 0.0)), float(data.get("lon", 0.0))
        delivery_id = data.get("delivery_id", "")
        status = data.get("delivery_status", "")

        try:
            target = get_target(delivery_id, status)
            if target and lat != 0.0 and lon != 0.0:
                lat, lon = move_towards(lat, lon, target)
                redis_client.hset(f"pos:{user_id}", mapping={"lat": str(lat), "lon": str(lon)})
            point = (
                Point("geo_position")
                .tag("user_id", str(user_id))
                .tag("delivery_id", str(delivery_id))
                .tag("vehicle_id", str(data.get("vehicle_id", "")))
                .field("lat", lat)
                .field("lon", lon)
                .field("delivery_status", status)
                .time(datetime.utcnow(), WritePrecision.NS)
            )
            write_api.write(bucket=influx_bucket, org=influx_org, record=point)
        except Exception as e:
            print(f"Tracking error for user {user_id}: {e}")
        time.sleep(5)

    active_threads.pop(user_id, None)


@location_bp.route("/start", methods=["POST"])
def start_tracking():
    data = request.get_json() or {}
    user_id = data.get('user_id')
    delivery_id = data.get('delivery_id')
    if not user_id or not delivery_id:
        return jsonify({"status": "error", "message": "user_id and delivery_id are required"}), 400

    mapping = {"delivery_id": delivery_id}
    if data.get('vehicle_id'):
        mapping["vehicle_id"] = data['vehicle_id']
    redis_client.hset(f"pos:{user_id}", mapping=mapping)

    if user_id in active_threads and active_threads[user_id].is_alive():
        return jsonify({"status": "already running"}), 200
    redis_client.set(f"tracking:{user_id}", "true")
    active_threads[user_id] = threading.Thread(target=tracking_loop, args=(user_id,))
    active_threads[user_id].start()
    return jsonify({"status": "started"}), 200


@location_bp.route("/stop", methods=["POST"])
def stop_tracking():
    user_id = (request.get_json() or {}).get('user_id')
    if not user_id:
        return jsonify({"error": "user_id required"}), 400
    redis_client.set(f"tracking:{user_id}", "false")
    return jsonify({"status": "stopped", "user_id": user_id}), 200
