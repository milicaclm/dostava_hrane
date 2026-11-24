from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import driver, redis_cache, invalidate_cache, get_user_role

user_bp = Blueprint('user', __name__)

try:
    with driver.session() as _session:
        _session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE")
except Exception:
    pass


def user_json(node):
    fields = ["name", "surname", "email", "phone_number", "account_type", "is_active"]
    result = {"id": node["id"], **{f: node[f] for f in fields}}
    for f in ["account_status", "motorcycle_license", "car_license", "salary", "average_rating"]:
        result[f] = node.get(f)
    result["is_available"] = node.get("is_available", False)
    return result


def is_forbidden(user_id):
    current_user_id = get_jwt_identity()
    with driver.session() as session:
        return user_id != current_user_id and get_user_role(session, current_user_id) != 'manager'


@user_bp.route('/<user_id>')
@jwt_required()
@redis_cache("user")
def get_user(user_id):
    with driver.session() as session:
        record = session.run("MATCH (u:User {id: $id}) RETURN u", id=user_id).single()
    if record:
        return jsonify(user_json(record["u"]))
    return jsonify({"error": "User not found"}), 404


@user_bp.route('/<user_id>/assign_vehicle/<vehicle_id>', methods=['POST'])
@jwt_required()
def assign_vehicle(user_id, vehicle_id):
    if is_forbidden(user_id):
        return jsonify({"error": "Forbidden"}), 403
    with driver.session() as session:
        if not session.run("MATCH (u:User {id: $id}) WHERE u.account_type IN ['courier','delivery'] RETURN u", id=user_id).single():
            return jsonify({"error": "User not found or invalid account_type"}), 404
        if not session.run("MATCH (v:Vehicle {id: $id}) RETURN v", id=vehicle_id).single():
            return jsonify({"error": "Vehicle not found"}), 404
        owner = session.run(
            "MATCH (u:User)-[:USES_VEHICLE]->(:Vehicle {id: $id}) RETURN u.id AS user_id LIMIT 1", id=vehicle_id
        ).single()
        if owner and owner["user_id"] == user_id:
            return jsonify({"message": "Vehicle already assigned to this user"})
        if owner:
            return jsonify({"error": "Vehicle already assigned to another user"}), 409
        session.run(
            "MATCH (u:User {id: $user_id}), (v:Vehicle {id: $vehicle_id}) CREATE (u)-[:USES_VEHICLE]->(v)",
            user_id=user_id, vehicle_id=vehicle_id
        )
    return jsonify({"message": "Vehicle assigned"})


@user_bp.route('/<user_id>/unassign_vehicle/<vehicle_id>', methods=['POST'])
@jwt_required()
def unassign_vehicle(user_id, vehicle_id):
    if is_forbidden(user_id):
        return jsonify({"error": "Forbidden"}), 403
    with driver.session() as session:
        res = session.run(
            "MATCH (u:User {id: $user_id})-[r:USES_VEHICLE]->(v:Vehicle {id: $vehicle_id}) DELETE r RETURN count(r) AS deleted_count",
            user_id=user_id, vehicle_id=vehicle_id
        ).single()
    if res["deleted_count"] > 0:
        return jsonify({"message": "Vehicle unassigned successfully"})
    return jsonify({"error": "No assignment found between user and vehicle"}), 404


def set_available(user_id, value):
    if is_forbidden(user_id):
        return jsonify({"error": "Forbidden"}), 403
    with driver.session() as session:
        record = session.run(
            "MATCH (u:User {id: $user_id}) WHERE u.account_type IN ['courier', 'delivery'] "
            "SET u.is_available = $value RETURN u",
            user_id=user_id, value=value
        ).single()
    if not record:
        return jsonify({"error": "Courier not found"}), 404
    return jsonify({"message": "Shift started" if value else "Shift ended"}), 200


@user_bp.route('/<user_id>/start_shift', methods=['POST'])
@jwt_required()
@invalidate_cache("user")
def start_shift(user_id):
    return set_available(user_id, True)


@user_bp.route('/<user_id>/end_shift', methods=['POST'])
@jwt_required()
@invalidate_cache("user")
def end_shift(user_id):
    return set_available(user_id, False)
