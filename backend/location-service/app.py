
from datetime import datetime
import os
from flask import Flask, jsonify, request
import requests
import jwt
from redis import Redis
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import threading
import time
import random

lock = threading.Lock()

app = Flask(__name__)

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


@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="ok"), 200

running = False


@app.route("/add_position", methods=["POST"])
def create_position_point():
    data = request.get_json()
    user_id = request.args.get("user_id")
    lat = data.get("lat")
    lon = data.get("lon")
    return (
        Point("geo_position")
        .tag("user_id", str(user_id))
        .field("lat", lat)
        .field("lon", lon)
        .time(datetime.utcnow(), WritePrecision.NS)
    )

#format vremena: 2024-06-01T12:00:00Z [YYYY-MM-DD'T'HH:MM:SS'Z']
@app.route("/delete_positions", methods=["DELETE"])
def delete_position_points():
    data = request.get_json()
    user_id = request.args.get("user_id")
    start_time = data.get("start_time")
    end_time = data.get("end_time")
    delete_query = f'''from(bucket: "{influx_bucket}")
  |> range(start: {start_time}, stop: {end_time})
  |> filter(fn: (r) => r["_measurement"] == "geo_position" and r["user_id"] == "{user_id}")
  |> drop()'''
    try:
        query_api.query(delete_query)
        return jsonify({"status": "positions deleted"}), 200
    except Exception as e:
        print(f"Error deleting positions: {e}")
        return jsonify({"status": "error"}), 500
    


@app.route("/set_position", methods=["POST"])
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
            mapping["delivery_id"] = data.get("delivery_id")
            redis_client.hset(f"pos:{uid}", mapping=mapping)
        except Exception as e:
            print(f"Error setting position: {e}")
            return jsonify({"status": "error"}), 500
    return jsonify({"status": "position updated"}), 200




def tracking_loop(user_id):
    global running

    count = 0

    while running:
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

        write_api.write(bucket=influx_bucket, org=influx_org, record=point)
        if count % 100 == 0:
            print(f"Written {count} points so far...")

        count += 1

        time.sleep(5)

    print(f"Stopped. Total points written: {count}")




@app.route("/start", methods=["POST"])
def start_tracking():
    global running
    # accept user_id from query or JSON body
    user_id = request.args.get('user_id') or data.get('user_id')
    data = request.get_json() or {}
    # require delivery_id (from query or JSON) so each point includes it
    delivery_id = request.args.get('delivery_id') or data.get('delivery_id')
    if not delivery_id:
        return jsonify({"status": "error", "message": "delivery_id is required"}), 400
    # require a user_id
    if not user_id:
        return jsonify({"status": "error", "message": "user_id is required"}), 400

    # verify user exists and is active via user-service
    try:
        resp = requests.get(f"http://user-service:8080/{user_id}", timeout=3)
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

    if running:
        return jsonify({"status": "already running"}), 200

    running = True

    thread = threading.Thread(
        target=tracking_loop,
        args=(user_id,)
    )
    thread.start()

    return jsonify({"status": "started"}), 200


@app.route("/stop", methods=["POST"])
def stop_tracking():
    global running
    running = False
    return jsonify({"status": "stopped"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)



