from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

# Service hosts (Docker service names)
USER_SVC = os.environ.get('USER_SVC', 'user-service')
RESOURCE_SVC = os.environ.get('RESOURCE_SVC', 'resource-service')
DELIVERY_SVC = os.environ.get('DELIVERY_SVC', 'delivery-service')

TARGET_PORT = os.environ.get('TARGET_PORT', '8080')

def proxy_request(target_base):
    path = request.full_path if request.query_string else request.path
    url = f"{target_base}{path}"
    headers = {k: v for k, v in request.headers.items() if k.lower() != 'host'}
    try:
        resp = requests.request(
            method=request.method,
            url=url,
            headers=headers,
            data=request.get_data(),
            allow_redirects=False,
            timeout=10
        )
    except requests.RequestException as e:
        return Response(f"Upstream request failed: {e}", status=502)

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    response_headers = [(name, value) for (name, value) in resp.headers.items() if name.lower() not in excluded_headers]
    return Response(resp.content, status=resp.status_code, headers=response_headers)


# Routing rules
@app.route('/users', defaults={'path': ''}, methods=['GET','POST','PUT','DELETE','PATCH'])
@app.route('/users/<path:path>', methods=['GET','POST','PUT','DELETE','PATCH'])
def users_proxy(path):
    target = f'http://{USER_SVC}:{TARGET_PORT}'
    return proxy_request(target)


@app.route('/resources', defaults={'path': ''}, methods=['GET','POST','PUT','DELETE','PATCH'])
@app.route('/resources/<path:path>', methods=['GET','POST','PUT','DELETE','PATCH'])
def resources_proxy(path):
    target = f'http://{RESOURCE_SVC}:{TARGET_PORT}'
    return proxy_request(target)


@app.route('/deliveries', defaults={'path': ''}, methods=['GET','POST','PUT','DELETE','PATCH'])
@app.route('/deliveries/<path:path>', methods=['GET','POST','PUT','DELETE','PATCH'])
def deliveries_proxy(path):
    target = f'http://{DELIVERY_SVC}:{TARGET_PORT}'
    return proxy_request(target)


@app.route('/vehicles', defaults={'path': ''}, methods=['GET','POST','PUT','DELETE','PATCH'])
@app.route('/vehicles/<path:path>', methods=['GET','POST','PUT','DELETE','PATCH'])
def vehicles_proxy(path):
    target = f'http://{DELIVERY_SVC}:{TARGET_PORT}'
    return proxy_request(target)


@app.route('/customers', defaults={'path': ''}, methods=['GET','POST','PUT','DELETE','PATCH'])
@app.route('/customers/<path:path>', methods=['GET','POST','PUT','DELETE','PATCH'])
def customers_proxy(path):
    target = f'http://{DELIVERY_SVC}:{TARGET_PORT}'
    return proxy_request(target)


@app.route('/')
def hello():
    return 'Gateway is running'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
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