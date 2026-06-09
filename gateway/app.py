import requests
import os
from flask import Flask, request, Response

app = Flask(__name__)

# Ako pokrećeš van Dockera, postavi BACKEND_URL=http://localhost:8080
BACKEND_URL = os.environ.get("BACKEND_URL", "http://delivery-subsystem:8080")

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    url = f"{BACKEND_URL}/{path}"
    # Prosleđivanje zahteva
    resp = requests.request(
        method=request.method,
        url=url,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    # Filtriranje headera
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    return Response(resp.content, resp.status_code, headers)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)