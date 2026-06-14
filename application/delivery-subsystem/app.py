import os
from flask import Flask, jsonify
from redis import Redis
from neo4j import GraphDatabase
from influxdb_client import InfluxDBClient
from flask_jwt_extended import JWTManager
from delivery import delivery_bp
from location import location_bp
from analitics import analitics_bp
from user import user_bp
from resource import resource_bp


app = Flask(__name__)

# JWT Konfiguracija
app.config['JWT_SECRET_KEY'] = 'dev-secret-key'
jwt = JWTManager(app)

# Inicijalizacija zajedničkih resursa
driver = GraphDatabase.driver(
    os.environ.get("NEO4J_URI", "bolt://neo4j:7687"), 
    auth=(os.environ.get("NEO4J_USERNAME", "neo4j"), os.environ.get("NEO4J_PASSWORD", "password"))
)

redis_client = Redis(
    host=os.environ.get("REDIS_HOST", "localhost"),
    port=int(os.environ.get("REDIS_PORT", 6379)),
    decode_responses=True
)

influx_client = InfluxDBClient(
    url=os.environ.get("INFLUXDB_URL", "http://localhost:8086"),
    token=os.environ.get("INFLUXDB_TOKEN", "mytoken123"),
    org=os.environ.get("INFLUXDB_ORG", "docs")
)

@app.route("/")
def hello():
    return jsonify({"status": "Delivery Subsystem is running"}), 200

# Ovde možete uvesti rute iz drugih fajlova koristeći Blueprints
# ili jednostavno prebaciti funkcije iz delivery.py i location.py ovde.
# Za početak, registrujmo blueprint ako ste ga definisali u routes.py:

app.register_blueprint(delivery_bp, url_prefix='/deliveries')
app.register_blueprint(location_bp, url_prefix='/locations')
app.register_blueprint(analitics_bp, url_prefix='/analitics')
app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(resource_bp, url_prefix='/resources')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
