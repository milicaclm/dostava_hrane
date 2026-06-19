#servis za upravljanje nalozima
import uuid
import os
from flask import Blueprint, jsonify, request
from neo4j import GraphDatabase
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

user_bp = Blueprint('user', __name__)


driver = GraphDatabase.driver(
    os.environ.get("NEO4J_URI", "bolt://neo4j:7687"), 
    auth=(os.environ.get("NEO4J_USERNAME", "neo4j"), os.environ.get("NEO4J_PASSWORD", "password"))
)

try:
    with driver.session() as _session:
        # ensure unique id constraint exists
        _session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE")
except Exception:
    # if Neo4j isn't ready yet, ignore — it will be created later
    pass




@user_bp.route('/')
def get_users():
    with driver.session() as session:
        result = session.run("MATCH (u:User) RETURN u")
        users = []
        for record in result:
            user_node = record["u"]
            users.append({
                "id": user_node["id"],
                "name": user_node["name"],
                "surname": user_node["surname"],
                "email": user_node["email"],
                "phone_number": user_node["phone_number"],
                "account_type": user_node["account_type"],
                "account_status": user_node.get("account_status"),
                "motorcycle_license": user_node.get("motorcycle_license"),
                "car_license": user_node.get("car_license"),
                "salary": user_node.get("salary"),
                "average_rating": user_node.get("average_rating"),
                "is_active": user_node["is_active"],
                "password": user_node["password"]
            })
    return jsonify(users)

@user_bp.route('/<user_id>')
def get_user(user_id):
    with driver.session() as session:
        result = session.run("MATCH (u:User {id: $user_id}) RETURN u", user_id=user_id)
        record = result.single()
        if record:
            user_node = record["u"]
            user = {
                "id": user_node["id"],
                "name": user_node["name"],
                "surname": user_node["surname"],
                "email": user_node["email"],
                "phone_number": user_node["phone_number"],
                "account_type": user_node["account_type"],
                "account_status": user_node.get("account_status"),
                "motorcycle_license": user_node.get("motorcycle_license"),
                "car_license": user_node.get("car_license"),
                "salary": user_node.get("salary"),
                "average_rating": user_node.get("average_rating"),
                "is_active": user_node["is_active"]
            }
            return jsonify(user)
        else:
            return jsonify({"error": "User not found"}), 404
        


@user_bp.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    with driver.session() as session:
        result = session.run(
            "MATCH (u:User {id: $user_id}) "
            "SET u.name = $name, u.surname = $surname, u.email = $email, u.phone_number = $phone_number, "
            "u.account_type = $account_type, u.is_active = $is_active, u.password = $password, "
            "u.account_status = $account_status, u.motorcycle_license = $motorcycle_license, "
            "u.car_license = $car_license, u.salary = $salary, u.average_rating = $average_rating "
            "RETURN u",
            user_id=user_id,
            name=data["name"],
            surname=data["surname"],
            email=data["email"],
            phone_number=data["phone_number"],
            account_type=data["account_type"],
            is_active=data["is_active"],
            account_status=data.get("account_status"),
            motorcycle_license=data.get("motorcycle_license"),
            car_license=data.get("car_license"),
            salary=data.get("salary"),
            average_rating=data.get("average_rating"),
            password=data["password"]
        )
        record = result.single()
        if record:
            user_node = record["u"]
            user = {
                "id": user_node["id"],
                "name": user_node["name"],
                "surname": user_node["surname"],
                "email": user_node["email"],
                "phone_number": user_node["phone_number"],
                "account_type": user_node["account_type"],
                "account_status": user_node.get("account_status"),
                "motorcycle_license": user_node.get("motorcycle_license"),
                "car_license": user_node.get("car_license"),
                "salary": user_node.get("salary"),
                "average_rating": user_node.get("average_rating"),
                "is_active": user_node["is_active"]
            }
            return jsonify(user)
        else:
            return jsonify({"error": "User not found"}), 404

@user_bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    with driver.session() as session:
        result = session.run("MATCH (u:User {id: $user_id}) DELETE u RETURN COUNT(u) AS deleted_count", user_id=user_id)
        record = result.single()
        if record["deleted_count"] > 0:
            return jsonify({"message": "User deleted successfully"})
        else:
            return jsonify({"error": "User not found"}), 404
        


@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    with driver.session() as session:
        result = session.run("MATCH (u:User {email: $email, password: $password}) RETURN u", email=email, password=password)
        record = result.single()
        if record:
            user_node = record["u"]
            access_token = create_access_token(identity=user_node["id"])
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401
        
@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    with driver.session() as session:
        # generate UUID if client didn't provide an id
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

@user_bp.route('/<user_id>/assign_vehicle/<license_plate>', methods=['POST'])
@jwt_required()
def assign_vehicle(user_id, license_plate):
    current_user_id = get_jwt_identity()
    with driver.session() as session:
        user_rec = session.run(
            "MATCH (u:User {id: $user_id}) WHERE u.account_type IN ['courier','delivery'] RETURN u",
            user_id=user_id
        ).single()
        if not user_rec:
            return jsonify({"error": "User not found or invalid account_type"}), 404

        vehicle_rec = session.run(
            "MATCH (v:Vehicle {license_plate: $license_plate}) RETURN v",
            license_plate=license_plate
        ).single()
        if not vehicle_rec:
            return jsonify({"error": "Vehicle not found"}), 404

        cnt = session.run(
            "MATCH (u:User {id: $user_id})-[r:USES_VEHICLE]->(v:Vehicle {license_plate: $license_plate}) RETURN count(r) AS cnt",
            user_id=user_id,
            license_plate=license_plate
        ).single()["cnt"]
        if cnt > 0:
            return jsonify({"message": "Vehicle already assigned to this user"})

        other = session.run(
            "MATCH (other:User)-[r:USES_VEHICLE]->(v:Vehicle {license_plate: $license_plate}) RETURN other.id AS other_id LIMIT 1",
            license_plate=license_plate
        ).single()
        if other and other.get("other_id") and other.get("other_id") != user_id:
            return jsonify({"error": "Vehicle already assigned to another user"}), 409
        
        res = session.run(
            "MATCH (u:User {id: $user_id}), (v:Vehicle {license_plate: $license_plate}) CREATE (u)-[:USES_VEHICLE]->(v) RETURN u, v",
            user_id=user_id,
            license_plate=license_plate
        ).single()
        if res:
            u = res["u"]
            v = res["v"]
            return jsonify({"message": "Vehicle assigned", "user": {"id": u.get("id")}, "vehicle": {"license_plate": v.get("license_plate")}})
        return jsonify({"error": "Could not assign vehicle"}), 500