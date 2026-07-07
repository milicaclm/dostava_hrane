from flask import Flask, Response, request
import os
import requests

app = Flask(__name__)

AUTH_SERVICE_URL = os.environ.get('AUTH_SERVICE_URL', 'http://auth-service:8080')
DELIVERY_SUBSYSTEM_URL = os.environ.get('DELIVERY_SUBSYSTEM_URL', 'http://delivery-subsystem:8080')

def proxy_request(base_url, path):
    url = f"{base_url}/{path}"
    print(f"--- Proxying request to: {url} ---")
    
    try:
        resp = requests.request(
            method=request.method,
            url=url,
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
            params=request.args
        )
        
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items()
                   if name.lower() not in excluded_headers]

        return Response(resp.content, resp.status_code, headers)
    except requests.exceptions.RequestException as e:
        print(f"--- Proxy error: {e} ---")
        import traceback
        traceback.print_exc()
        return Response(f"Proxy error: {str(e)}", status=502)

@app.route('/')
def serve_login():
    return proxy_request(AUTH_SERVICE_URL, "")

@app.route('/api/auth-service/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_auth_api(path):
    return proxy_request(AUTH_SERVICE_URL, path)

@app.route('/manager/')
@app.route('/manager/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_manager(path=""):
    return proxy_request(DELIVERY_SUBSYSTEM_URL, f"manager/{path}")

@app.route('/courier/')
@app.route('/courier/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_courier(path=""):
    return proxy_request(DELIVERY_SUBSYSTEM_URL, f"courier/{path}")

@app.route('/api/delivery-subsystem/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/api/delivery-service/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_delivery_api(path):
    return proxy_request(DELIVERY_SUBSYSTEM_URL, path)

@app.route('/static/<path:path>')
def proxy_static(path):
    return proxy_request(AUTH_SERVICE_URL, f"static/{path}")

@app.route('/favicon.ico')
def favicon():
    return Response(status=204, mimetype='image/x-icon')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)