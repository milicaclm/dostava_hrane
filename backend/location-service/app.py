
from datetime import datetime
import os
from flask import Flask, jsonify, request
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
influx_bucket = os.environ.get("INFLUXDB_BUCKET", "home")

influx_client = InfluxDBClient(url=influx_url, token=influx_token, org=influx_org)
write_api = influx_client.write_api(write_options=SYNCHRONOUS)
query_api = influx_client.query_api()


@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="ok"), 200

running = False
current_lat = 0.
current_lon = 0.


@app.route("/set_position", methods=["POST"])
def set_position():
    """korisnik zadaje noviju vrednost kada zeli"""
    global current_lat, current_lon
    data = request.get_json()
    with lock:
        current_lat = data.get("lat", 0.)
        current_lon = data.get("lon", 0.)
    return jsonify({"status": "position updated"}), 200



def tracking_loop(user_id):
    global running

    count = 0

    while running:
        with lock:
            lat = current_lat
            lon = current_lon

        point = (
            Point("gps_position")
            .tag("user_id", str(user_id))
            .field("lat", lat)
            .field("lon", lon)
            .time(datetime.utcnow(), WritePrecision.NS)
        )

        write_api.write(bucket=influx_bucket, org=influx_org, record=point)
        if count % 100 == 0:
            print(f"Written {count} points so far...")

        count += 1

        time.sleep(1)

    print(f"Stopped. Total points written: {count}")



@app.route("/start", methods=["POST"])
def start_tracking():
    global running
    global current_lat, current_lon

    data = request.get_json()
    user_id = data.get("user_id", "1")
    current_lat, current_lon = data.get("lat", 0.), data.get("lon", 0.)

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



