import requests
from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, API Gateway!"


# Minimalne proxy rute koje stvarno prosleđuju zahteve
@app.route("/user")
def user_service():
    res = requests.get("http://user-service:8081/")
    return (res.content, res.status_code, res.headers.items())


@app.route("/resource")
def resource_service():
    res = requests.get("http://resource-service:8082/")
    return (res.content, res.status_code, res.headers.items())


@app.route("/delivery")
def delivery_service():
    res = requests.get("http://delivery-service:8083/")
    return (res.content, res.status_code, res.headers.items())


@app.route("/location")
def location_service():
    res = requests.get("http://location-service:8084/")
    return (res.content, res.status_code, res.headers.items())


@app.route("/analytics")
def analytics_service():
    res = requests.get("http://analytics-service:8085/")
    return (res.content, res.status_code, res.headers.items())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)