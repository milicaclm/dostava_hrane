from flask import Blueprint, request, jsonify
import os
from influxdb_client import InfluxDBClient

analitics_bp = Blueprint('analitics', __name__)


# InfluxDB configuration via env
influx_url = os.environ.get('INFLUXDB_URL', 'http://localhost:8086')
influx_token = os.environ.get('INFLUXDB_TOKEN', 'mytoken123')
influx_org = os.environ.get('INFLUXDB_ORG', 'docs')
influx_bucket = os.environ.get("INFLUXDB_BUCKET", "geo_data")


client = InfluxDBClient(url=influx_url, token=influx_token, org=influx_org)
write_api = client.write_api()



@analitics_bp.route('/health', methods=['GET'])
def health():
	return jsonify(status='ok')


@analitics_bp.route('/efficiency', methods=['GET'])
def analiza_efikasnosti():
	data = request.get_json() or {}
	user_id = data.get('user_id')
	if not user_id:
		return jsonify({"error": "user_id is required"}), 400
	delivery_id = data.get('delivery_id')
	query = f'''from(bucket: "{influx_bucket}")
  |> range(start: -1h)
  |> filter(fn: (r) => r["_measurement"] == "geo_position" and r["user_id"] == "{user_id}")
  |> group(columns: ["status", "delivery_id"])
  |> limit(n: 2)
  |> elapsed(unit: 1s, timeColumn: "_time", columnName: "trajanje_dostave")
  |> filter(fn: (r) => exists r.trajanje_dostave)
  |> group(columns: ["status"])
  |> mean(column: "trajanje_dostave")'''

	try:
		tables = client.query_api().query(query, org=influx_org)
		res = []
		for table in tables:
			for record in table.records:
				res.append({"status": record.values.get("status"), "average_duration": record.get_value()})
		return jsonify(res)
	except Exception as e:
		return jsonify({"error": str(e)}), 500
