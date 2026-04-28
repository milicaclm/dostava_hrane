# API Gateway

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, API Gateway!"

# Proxy rute ka mikroservisima
@app.route('/user')
def user_service():
    return {"service": "user-service", "port": 8080}

@app.route('/resource')
def resource_service():
    return {"service": "resource-service", "port": 8081}

@app.route('/delivery')
def delivery_service():
    return {"service": "delivery-service", "port": 8082}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)