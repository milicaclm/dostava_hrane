import requests
import os
from flask import Flask, request, Response

app = Flask(__name__)

# Definisanje URL-ova za svaki podsistem u Docker mreži
DELIVERY_SUBSYSTEM_URL = os.environ.get("DELIVERY_SUBSYSTEM_URL", "http://delivery-subsystem:8080")

# Kada dodaš nove podsisteme, dodaj ih ovde:
# USER_SUBSYSTEM_URL = os.environ.get("USER_SUBSYSTEM_URL", "http://user-subsystem:8080")

def forward_request(base_url, path):
    url = f"{base_url}/{path}"
    # Prosleđivanje zahteva sa svim zaglavljima, podacima i parametrima
    resp = requests.request(
        method=request.method,
        url=url,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False,
        params=request.args
    )

    # Filtriranje headera (neophodno da se izbegnu greške pri proksiranju)
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    return Response(resp.content, resp.status_code, headers)

@app.route('/api/delivery-subsystem/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/api/delivery-subsystem/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_delivery(path):
    return forward_request(DELIVERY_SUBSYSTEM_URL, path)

# Primer rute za budući podsistem:
# @app.route('/api/user/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
# @app.route('/api/user/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
# def proxy_user(path):
#     return forward_request(USER_SUBSYSTEM_URL, path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)