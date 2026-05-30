
import os
from flask import Flask, jsonify, request
from redis import Redis
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

app = Flask(__name__)

# --- REDIS CONFIG ---
redis_client = Redis(
    host=os.environ.get("REDIS_HOST", "localhost"),
    port=int(os.environ.get("REDIS_PORT", 6379)),
    decode_responses=True
)

# --- INFLUXDB CONFIG ---
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

def save_location(user_id, latitude, longitude):
    point = Point("user_location")
    point.tag("user_id", user_id)
    point.field("latitude", latitude)
    point.field("longitude", longitude)
    write_api.write(bucket=influx_bucket, record=point)

def get_location(user_id):
    query = f'from(bucket: "{influx_bucket}") |> range(start: -1h) |> filter(fn: (r) => r._measurement == "user_location" and r.user_id == "{user_id}") |> last()'
    result = query_api.query(org=influx_org, query=query)
    results = []
    for table in result:
        for record in table.records:
            results.append(
                {
                    "user_id": record.values["user_id"],
                    "latitude": record.values["latitude"],
                    "longitude": record.values["longitude"],
                    "time": record.values["_time"].isoformat()
                }
            )
    return results[0] if results else None

def delete_location(user_id):
    query = f'from(bucket: "{influx_bucket}") |> range(start: -1h) |> filter(fn: (r) => r._measurement == "user_location" and r.user_id == "{user_id}") |> last()'
    result = query_api.query(org=influx_org, query=query)
    for table in result:
        for record in table.records:
            delete_query = f'from(bucket: "{influx_bucket}") |> range(start: -1h) |> filter(fn: (r) => r._measurement == "user_location" and r.user_id == "{user_id}" and r._time == {record.values["_time"].isoformat()}) |> drop()'
            query_api.query(org=influx_org, query=delete_query)





if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)



