import os
from flask import Flask, jsonify, send_from_directory
from flask_jwt_extended import JWTManager
from delivery import delivery_bp
from location import location_bp
from analitics import analitics_bp
from user import user_bp
from resource import resource_bp
from db import driver, redis_client, influx_client


app = Flask(__name__)

# JWT Konfiguracija
app.config['JWT_SECRET_KEY'] = 'dev-secret-key'
jwt = JWTManager(app)

@app.route("/")
def hello():
    return jsonify({"status": "Delivery Subsystem is running"}), 200

# --- Rutiranje Frontend Aplikacija ---

@app.route('/manager/')
def serve_manager_index():
    return send_from_directory('delivery-manager-front/templates', 'index.html')

@app.route('/manager/<path:path>')
def serve_manager_files(path):
    if path.startswith('static/'):
        return send_from_directory('delivery-manager-front', path)
    return send_from_directory('delivery-manager-front/templates', path)

@app.route('/courier/')
def serve_courier_index():
    return send_from_directory('courier-front/templates', 'index.html')

@app.route('/courier/<path:path>')
def serve_courier_files(path):
    if path.startswith('static/'):
        return send_from_directory('courier-front', path)
    return send_from_directory('courier-front/templates', path)

# --- Registracija API Blueprints ---

app.register_blueprint(delivery_bp, url_prefix='/deliveries')
app.register_blueprint(location_bp, url_prefix='/locations')
app.register_blueprint(analitics_bp, url_prefix='/analitics')
app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(resource_bp, url_prefix='/resources')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)