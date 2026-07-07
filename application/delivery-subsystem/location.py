
from datetime import datetime
import os
from flask import Blueprint, jsonify, request
import requests
from influxdb_client import Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import threading
from influxdb_client.client.delete_api import DeleteApi
import time
import random

lock = threading.Lock()

active_threads = {}

location_bp = Blueprint('location', __name__)

from db import redis_client, influx_client, influx_bucket, influx_org

write_api = influx_client.write_api(write_options=SYNCHRONOUS)
query_api = influx_client.query_api()
delete_api = influx_client.delete_api()

INTERNAL_API_URL = os.environ.get("INTERNAL_API_URL", "http://localhost:8080")

@location_bp.route("/health", methods=["GET"])
def health():
    return jsonify(status="ok"), 200


@location_bp.route("/add_position", methods=["POST"])
def create_position_point():
    data = request.get_json()
    user_id = request.args.get("user_id") or data.get("user_id")
    lat = data.get("lat")
    lon = data.get("lon")
    
    if not user_id or lat is None or lon is None:
        return jsonify({"error": "Missing parameters"}), 400

    point = (
        Point("geo_position")
        .tag("user_id", str(user_id))
        .field("lat", lat)
        .field("lon", lon)
        .time(datetime.utcnow(), WritePrecision.NS)
    )
    try:
        write_api.write(bucket=influx_bucket, org=influx_org, record=point)
        return jsonify({"status": "position added"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@location_bp.route("/get_positions", methods=["GET"])
def get_positions():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
    
    query = f'''
        from(bucket: "{influx_bucket}")
        |> range(start: -24h)
        |> filter(fn: (r) => r["_measurement"] == "geo_position")
        |> filter(fn: (r) => r["user_id"] == "{user_id}")
        |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
    '''
    try:
        result = query_api.query(org=influx_org, query=query)
        output = []
        for table in result:
            for record in table.records:
                output.append(record.values)
        return jsonify(output), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@location_bp.route("/current_position", methods=["GET"])
def current_position():
    """Vraća trenutnu poziciju kurira direktno iz Redis hash-a (real-time, bez InfluxDB upita)."""
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
    try:
        data = redis_client.hgetall(f"pos:{user_id}")
        if not data:
            return jsonify(None), 200
        return jsonify({
            "lat": data.get("lat"),
            "lon": data.get("lon"),
            "delivery_id": data.get("delivery_id"),
            "delivery_status": data.get("delivery_status"),
            "vehicle_id": data.get("vehicle_id"),
            "last_seen": data.get("last_seen")
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@location_bp.route("/delete_positions", methods=["DELETE"])
def delete_position_points():
    data = request.get_json()
    user_id = request.args.get("user_id")
    start_time = data.get("start_time")
    end_time = data.get("end_time")

    if not all([user_id, start_time, end_time]):
        return jsonify({"error": "Missing start_time, end_time or user_id"}), 400

    try:
        delete_api.delete(
            start_time, 
            end_time, 
            f'_measurement="geo_position" AND user_id="{user_id}"',
            bucket=influx_bucket, 
            org=influx_org
        )
        return jsonify({"status": "positions deleted"}), 200
    except Exception as e:
        print(f"Error deleting positions: {e}")
        return jsonify({"status": "error"}), 500


@location_bp.route("/set_position", methods=["POST"])
def set_position():
    """korisnik zadaje noviju vrednost kada zeli"""
    data = request.get_json() or {}
    with lock:
        try:
            uid = request.args.get('user_id')
            mapping = {
                "lat": data.get("lat", 0.0),
                "lon": data.get("lon", 0.0),
                "last_seen": datetime.utcnow().isoformat() + "Z"
            }
            mapping["user_id"] = uid
            if data.get("delivery_id") is not None:
                mapping["delivery_id"] = data.get("delivery_id")
            if data.get("vehicle_id") is not None:
                mapping["vehicle_id"] = data.get("vehicle_id")
            redis_client.hset(f"pos:{uid}", mapping=mapping)
        except Exception as e:
            print(f"Error setting position: {e}")
            return jsonify({"status": "error"}), 500
    return jsonify({"status": "position updated"}), 200




def tracking_loop(user_id):
    count = 0
    while redis_client.get(f"tracking:{user_id}") == "true":
        data = redis_client.hgetall(f"pos:{user_id}")
        if not data:
            time.sleep(1)
            continue
        try:
            lat = float(data.get("lat", 0.0))
            lon = float(data.get("lon", 0.0))
        except Exception:
            lat = 0.0
            lon = 0.0
        delivery_id = data.get("delivery_id", "")
        delivery_status = data.get("delivery_status", "")
        vehicle_id = data.get("vehicle_id", "")

        target_lat = None
        target_lon = None
        if delivery_id:
            from db import driver
            try:
                with driver.session() as session:
                    res = session.run("MATCH (d:Delivery {id: $id}) RETURN d", id=delivery_id).single()
                    if res:
                        d = res["d"]
                        r_lat = d.get("restaurant_lat")
                        r_lon = d.get("restaurant_lon")
                        c_lat = d.get("customer_lat")
                        c_lon = d.get("customer_lon")
                        
                        if delivery_status == "accepted" and r_lat is not None:
                            target_lat = float(r_lat)
                            target_lon = float(r_lon)
                        elif delivery_status in ["in transit", "in_transit"] and c_lat is not None:
                            target_lat = float(c_lat)
                            target_lon = float(c_lon)
            except Exception as db_err:
                print(f"Error fetching delivery details for simulation: {db_err}")

        if target_lat is not None and target_lon is not None and lat != 0.0 and lon != 0.0:
            import math
            d_lat = target_lat - lat
            d_lon = target_lon - lon
            distance = math.sqrt(d_lat**2 + d_lon**2)
            if distance > 0.0001:
                step = 0.0008
                if distance <= step:
                    lat = target_lat
                    lon = target_lon
                else:
                    lat += (d_lat / distance) * step
                    lon += (d_lon / distance) * step
                
                try:
                    redis_client.hset(f"pos:{user_id}", mapping={
                        "lat": str(lat),
                        "lon": str(lon)
                    })
                except Exception as redis_err:
                    print(f"Error updating simulated position in Redis: {redis_err}")

        point = (
            Point("geo_position")
            .tag("user_id", str(user_id))
            .tag("delivery_id", str(delivery_id))
            .tag("vehicle_id", str(vehicle_id))
            .field("lat", lat)
            .field("lon", lon)
            .field("delivery_status", delivery_status)
            .time(datetime.utcnow(), WritePrecision.NS)
        )

        try:
            write_api.write(bucket=influx_bucket, org=influx_org, record=point)
            if count % 100 == 0:
                print(f"Written {count} points so far...")
            count += 1
        except Exception as e:
            print(f"Error writing to InfluxDB for user {user_id}: {e}")

        time.sleep(5)

    active_threads.pop(user_id, None)
    print(f"Stopped tracking for {user_id}. Total points written: {count}")



@location_bp.route("/start", methods=["POST"])
def start_tracking():
    data = request.get_json() or {}
    user_id = request.args.get('user_id') or data.get('user_id')
    delivery_id = request.args.get('delivery_id') or data.get('delivery_id')
    vehicle_id = request.args.get('vehicle_id') or data.get('vehicle_id')
    if not delivery_id:
        return jsonify({"status": "error", "message": "delivery_id is required"}), 400
    if not user_id:
        return jsonify({"status": "error", "message": "user_id is required"}), 400

    try:
        resp = requests.get(f"{INTERNAL_API_URL}/users/{user_id}", timeout=3)
        if resp.status_code != 200:
            return jsonify({"status": "error", "message": "user not found or not active"}), 404
    except requests.RequestException:
        return jsonify({"status": "error", "message": "user-service unreachable"}), 503

    existing = redis_client.hgetall(f"pos:{user_id}")
    try:
        mapping = {"delivery_id": delivery_id}
        if vehicle_id:
            mapping["vehicle_id"] = vehicle_id
        redis_client.hset(f"pos:{user_id}", mapping=mapping)
        existing = redis_client.hgetall(f"pos:{user_id}")
    except Exception as e:
        print(f"Error setting delivery_id: {e}")
        return jsonify({"status": "error", "message": "failed to persist delivery_id"}), 500
    if not existing:
        return jsonify({"status": "error", "message": "no position data for user; start aborted"}), 400

    if redis_client.get(f"tracking:{user_id}") == "true":
        if user_id in active_threads and active_threads[user_id].is_alive():
            return jsonify({"status": "already running"}), 200

    redis_client.set(f"tracking:{user_id}", "true")

    thread = threading.Thread(
        target=tracking_loop,
        args=(user_id,)
    )
    active_threads[user_id] = thread
    thread.start()

    return jsonify({"status": "started"}), 200


@location_bp.route("/stop", methods=["POST"])
def stop_tracking():
    data = request.get_json() or {}
    user_id = data.get('user_id') or request.args.get('user_id')
    if user_id:
        redis_client.set(f"tracking:{user_id}", "false")
        return jsonify({"status": "stopped", "user_id": user_id}), 200
    return jsonify({"error": "user_id required"}), 400
