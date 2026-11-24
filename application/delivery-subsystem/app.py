import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from delivery import delivery_bp
from location import location_bp
from analytics import analytics_bp
from user import user_bp
from resource import resource_bp
from scheduler import scheduler_bp
from front_routes import manager_front_bp, courier_front_bp
from db import driver, redis_client, influx_client


app = Flask(__name__)

@app.template_filter('fmt_dt')
def fmt_dt_filter(val):
    if not val:
        return '—'
    s = str(val).replace('T', ' ')
    try:
        date_part, time_part = s[:10], s[11:16]
        y, m, d = date_part.split('-')
        return f"{d}.{m}.{y} {time_part}"
    except Exception:
        return s[:16]

@app.template_filter('fmt_status')
def fmt_status_filter(val):
    return {
        'placed': 'Kreirana', 'offered': 'Ponuđena', 'pending': 'Na čekanju',
        'accepted': 'Prihvaćena', 'in transit': 'U dostavi',
        'completed': 'Isporučena', 'cancelled': 'Otkazana',
    }.get(str(val).lower(), val or '—')

@app.template_filter('fmt_vehicle')
def fmt_vehicle_filter(val):
    return {
        'bicycle': 'Bicikl', 'bike': 'Bicikl',
        'motorcycle': 'Motor', 'scooter': 'Skuter', 'car': 'Automobil',
    }.get(str(val).lower(), val or '—')

app.config['JWT_SECRET_KEY'] = 'dev-secret-key'
jwt = JWTManager(app)

@app.route("/")
def hello():
    return jsonify({"status": "Delivery Subsystem is running"}), 200


app.register_blueprint(manager_front_bp, url_prefix='/manager')
app.register_blueprint(courier_front_bp, url_prefix='/courier')


app.register_blueprint(delivery_bp, url_prefix='/deliveries')
app.register_blueprint(scheduler_bp, url_prefix='/scheduler')
app.register_blueprint(location_bp, url_prefix='/locations')
app.register_blueprint(analytics_bp, url_prefix='/analytics')
app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(resource_bp, url_prefix='/resources')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)