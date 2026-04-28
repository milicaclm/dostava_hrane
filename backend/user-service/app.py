#servis za upravljanje nalozima

from flask import *
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from neo4j import GraphDatabase

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, User Service!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
