import os
from flask import Flask, jsonify, request, Blueprint, render_template, redirect, make_response
from neo4j import GraphDatabase
from flask_jwt_extended import create_access_token, JWTManager
import uuid

app = Flask(__name__, template_folder='templates', static_folder='static')

auth_bp = Blueprint('auth', __name__)

from datetime import timedelta
app.config['JWT_SECRET_KEY'] = 'dev-secret-key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=20)
jwt = JWTManager(app)

driver = GraphDatabase.driver(
    os.environ.get("NEO4J_URI", "bolt://neo4j:7687"), 
    auth=(os.environ.get("NEO4J_USERNAME", "neo4j"), os.environ.get("NEO4J_PASSWORD", "password"))
)

try:
    with driver.session() as _session:
        _session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE")
except Exception:
    pass

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        with driver.session() as session:
            result = session.run("MATCH (u:User {email: $email, password: $password}) RETURN u", email=email, password=password)
            record = result.single()
            if record:
                user_node = record["u"]
                account_type = user_node["account_type"]
                if account_type == 'manager':
                    target = '/manager/'
                elif account_type == 'courier':
                    target = '/courier/'
                else:
                    return render_template('login.html', error='Tip naloga nije podržan za prijavu.')
                access_token = create_access_token(
                    identity=user_node["id"],
                    additional_claims={"account_type": account_type}
                )
                resp = make_response(redirect(target))
                resp.set_cookie('jwt_token', access_token, httponly=True, path='/', samesite='Lax')
                return resp
            return render_template('login.html', error='Pogrešan email ili lozinka.')
    return render_template('login.html')

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    resp = make_response(redirect('/'))
    resp.delete_cookie('jwt_token', path='/')
    return resp

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    with driver.session() as session:
        user_id = data.get("id") if data.get("id") else str(uuid.uuid4())
        session.run(
            "CREATE (u:User {id: $id, name: $name, surname: $surname, email: $email, phone_number: $phone_number, "
            "account_type: $account_type, is_active: $is_active, password: $password, account_status: $account_status, "
            "motorcycle_license: $motorcycle_license, car_license: $car_license, salary: $salary, average_rating: $average_rating})",
            id=user_id,
            name=data["name"],
            surname=data["surname"],
            email=data["email"],
            phone_number=data["phone_number"],
            account_type=data["account_type"],
            is_active=data["is_active"],
            password=data["password"],
            account_status=data.get("account_status", "active"),
            motorcycle_license=data.get("motorcycle_license", False),
            car_license=data.get("car_license", False),
            salary=data.get("salary", 0),
            average_rating=data.get("average_rating", 0)
        )
    return jsonify({"message": "User created successfully", "id": user_id}), 201

app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)