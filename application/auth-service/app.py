import os
from flask import Flask, jsonify, request, Blueprint, render_template
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

@app.route("/")
def index():
    return render_template('login.html')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    with driver.session() as session:
        result = session.run("MATCH (u:User {email: $email, password: $password}) RETURN u", email=email, password=password)
        record = result.single()
        if record:
            user_node = record["u"]
            additional_claims = {"account_type": user_node["account_type"]}
            access_token = create_access_token(identity=user_node["id"], additional_claims=additional_claims)
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401
        
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