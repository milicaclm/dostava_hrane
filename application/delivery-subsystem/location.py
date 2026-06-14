
from datetime import datetime
import os
from flask import Blueprint, jsonify, request
import requests
from redis import Redis
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import threading
from influxdb_client.client.delete_api import DeleteApi
import time
import random

lock = threading.Lock()

# Pratimo pokrenute niti u memoriji kako bismo izbegli dupliranje
active_threads = {}

location_bp = Blueprint('location', __name__)

redis_client = Redis(
    host=os.environ.get("REDIS_HOST", "localhost"),
    port=int(os.environ.get("REDIS_PORT", 6379)),
    decode_responses=True
)


influx_url = os.environ.get("INFLUXDB_URL", "http://localhost:8086")
influx_token = os.environ.get("INFLUXDB_TOKEN", "mytoken123")
influx_org = os.environ.get("INFLUXDB_ORG", "docs")
influx_bucket = os.environ.get("INFLUXDB_BUCKET", "geo_data")

influx_client = InfluxDBClient(url=influx_url, token=influx_token, org=influx_org)
write_api = influx_client.write_api(write_options=SYNCHRONOUS)
query_api = influx_client.query_api()
delete_api = influx_client.delete_api()

# Koristi se za interne pozive ka drugim modulima (npr. provera korisnika)
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

#format vremena: 2024-06-01T12:00:00Z [YYYY-MM-DD'T'HH:MM:SS'Z']
@location_bp.route("/delete_positions", methods=["DELETE"])
def delete_position_points():
    data = request.get_json()
    user_id = request.args.get("user_id")
    start_time = data.get("start_time")
    end_time = data.get("end_time")

    if not all([user_id, start_time, end_time]):
        return jsonify({"error": "Missing start_time, end_time or user_id"}), 400

    try:
        # InfluxDB delete API expects datetime objects or strings in RFC3339
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
    data = request.get_json()
    # delivery_id is required for position updates
    if data is None or data.get("delivery_id") is None:
        return jsonify({"status": "error", "message": "delivery_id is required"}), 400
    with lock:
        try:
            uid = request.args.get('user_id')
            # update lat/lon and optionally delivery_id here
            mapping = {
                "lat": data.get("lat", 0.0),
                "lon": data.get("lon", 0.0),
                "last_seen": datetime.utcnow().isoformat() + "Z"
            }
            # delivery_id present (enforced above) — add to mapping
            mapping["user_id"] = uid
            mapping["delivery_id"] = data.get("delivery_id")
            redis_client.hset(f"pos:{uid}", mapping=mapping)
        except Exception as e:
            print(f"Error setting position: {e}")
            return jsonify({"status": "error"}), 500
    return jsonify({"status": "position updated"}), 200




def tracking_loop(user_id):
    count = 0
    while redis_client.get(f"tracking:{user_id}") == "true":
        # read enriched hash from redis
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

        point = (
            Point("geo_position")
            .tag("user_id", str(user_id))
            .tag("delivery_id", str(delivery_id))
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
    # accept user_id from query or JSON body
    user_id = request.args.get('user_id') or data.get('user_id')
    # require delivery_id (from query or JSON) so each point includes it
    delivery_id = request.args.get('delivery_id') or data.get('delivery_id')
    if not delivery_id:
        return jsonify({"status": "error", "message": "delivery_id is required"}), 400
    # require a user_id
    if not user_id:
        return jsonify({"status": "error", "message": "user_id is required"}), 400

    # Provera korisnika unutar istog subsystema
    try:
        # Putanja mora odgovarati prefiksu registrovanom u app.py (/users)
        resp = requests.get(f"{INTERNAL_API_URL}/users/{user_id}", timeout=3)
        if resp.status_code != 200:
            return jsonify({"status": "error", "message": "user not found or not active"}), 404
    except requests.RequestException:
        return jsonify({"status": "error", "message": "user-service unreachable"}), 503

    # require existing position data in Redis before starting
    existing = redis_client.hgetall(f"pos:{user_id}")
    # persist provided delivery_id into the Redis hash (add to mapping)
    try:
        redis_client.hset(f"pos:{user_id}", mapping={"delivery_id": delivery_id})
        # refresh existing map for subsequent checks
        existing = redis_client.hgetall(f"pos:{user_id}")
    except Exception as e:
        print(f"Error setting delivery_id: {e}")
        return jsonify({"status": "error", "message": "failed to persist delivery_id"}), 500
    if not existing:
        return jsonify({"status": "error", "message": "no position data for user; start aborted"}), 400
    # delivery_id and delivery_status (if any) are expected to be set by delivery-service

    if redis_client.get(f"tracking:{user_id}") == "true":
        # Provera da li je nit već aktivna u trenutnom procesu
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
