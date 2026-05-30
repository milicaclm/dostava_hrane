from flask import Flask, request, jsonify
import os
from influxdb_client import InfluxDBClient

app = Flask(__name__)

# InfluxDB configuration via env
influx_url = os.environ.get('INFLUXDB_URL', 'http://localhost:8086')
influx_token = os.environ.get('INFLUXDB_TOKEN', 'mytoken123')
influx_org = os.environ.get('INFLUXDB_ORG', 'docs')

client = InfluxDBClient(url=influx_url, token=influx_token, org=influx_org)


@app.route('/health', methods=['GET'])
def health():
	return jsonify(status='ok')


if __name__ == '__main__':
	port = int(os.environ.get('PORT', 8080))
	app.run(host='0.0.0.0', port=port)
