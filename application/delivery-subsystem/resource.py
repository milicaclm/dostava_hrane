import uuid
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import driver, invalidate_cache, get_user_role

resource_bp = Blueprint('resource', __name__)


def courier_json(node):
    result = {f: node[f] for f in ["id", "name", "surname", "email", "phone_number", "is_active"]}
    result["motorcycle_license"] = node.get("motorcycle_license", False)
    result["car_license"] = node.get("car_license", False)
    result["salary"] = node.get("salary", 0.0)
    result["average_rating"] = node.get("average_rating", 0.0)
    return result


def vehicle_json(node, in_use=None, **extra):
    result = {f: node.get(f) for f in ["id", "owner_id", "type", "license_plate", "is_ready", "brand", "model", "color", "description"]}
    if in_use is not None:
        result["in_use"] = in_use
    return {**result, **extra}


def product_json(node):
    return {f: node[f] for f in ["id", "name", "description", "price"]}


def vehicle_access_error(session, vehicle_id):
    user_id = get_jwt_identity()
    role = get_user_role(session, user_id)
    if not role:
        return jsonify({"error": "User role not found."}), 403
    record = session.run("MATCH (v:Vehicle {id: $id}) RETURN v.owner_id AS owner_id", id=vehicle_id).single()
    if not record:
        return jsonify({"error": "Vehicle not found"}), 404
    owner_id = record["owner_id"]
    if owner_id != user_id and not (role == 'manager' and owner_id is None):
        return jsonify({"error": "Forbidden"}), 403
    return None


VEHICLE_FIELDS = "v.license_plate = $license_plate, v.type = $type, v.is_ready = $is_ready, " \
                 "v.brand = $brand, v.model = $model, v.color = $color, v.description = $description"


def vehicle_params(data):
    return dict(
        license_plate=data.get("license_plate", ""), type=data["type"].lower(), is_ready=data.get("is_ready", True),
        brand=data.get("brand"), model=data.get("model"), color=data.get("color"), description=data.get("description")
    )


@resource_bp.route('/vehicles')
@jwt_required()
def get_vehicles():
    owner_id = request.args.get('owner_id')
    match = "MATCH (v:Vehicle)"
    if owner_id:
        match = """
            MATCH (v:Vehicle)
            WHERE COALESCE(v.is_ready, true) = true AND (
                v.owner_id = $owner_id
                OR (v.owner_id IS NULL AND (
                    NOT EXISTS { ()-[:USES_VEHICLE]->(v) }
                    OR EXISTS { (:User {id: $owner_id})-[:USES_VEHICLE]->(v) }
                ))
            )
        """
    query = match + """
        OPTIONAL MATCH (v)<-[:USES_VEHICLE]-(u_assigned:User)
        WITH v, u_assigned.id AS assigned_user_id
        OPTIONAL MATCH (v)<-[:USES_VEHICLE]-(u:User)-[r:OFFERED]->(d:Delivery)
        WHERE r.status IN ['accepted', 'in transit']
        WITH v, assigned_user_id, count(d) > 0 AS is_in_use
        RETURN v, assigned_user_id, is_in_use
    """
    with driver.session() as session:
        result = session.run(query, owner_id=owner_id)
        vehicles = [vehicle_json(r["v"], r["is_in_use"], assigned_user_id=r["assigned_user_id"]) for r in result]
    return jsonify({"vehicles": vehicles})


@resource_bp.route('/vehicles', methods=['POST'])
@jwt_required()
def create_vehicle():
    user_id = get_jwt_identity()
    data = request.get_json()
    if not data.get("type"):
        return jsonify({"error": "Type is required"}), 400

    with driver.session() as session:
        role = get_user_role(session, user_id)
        if not role:
            return jsonify({"error": "User role not found."}), 403
        owner_param = data.get("owner_id")
        if owner_param == "me":
            owner_id = user_id
        elif owner_param is None and role == 'manager':
            owner_id = None
        else:
            return jsonify({"error": "Forbidden"}), 403

        vehicle_id = f"v-{uuid.uuid4().hex[:8]}"
        session.run(
            "CREATE (v:Vehicle {id: $id, owner_id: $owner_id, license_plate: $license_plate, type: $type, "
            "is_ready: $is_ready, brand: $brand, model: $model, color: $color, description: $description})",
            id=vehicle_id, owner_id=owner_id, **vehicle_params(data)
        )
    return jsonify({"message": "Vehicle created successfully", "id": vehicle_id}), 201


@resource_bp.route('/vehicles/<vehicle_id>/update', methods=['PUT'])
@jwt_required()
def update_vehicle(vehicle_id):
    data = request.get_json()
    if not data.get("type"):
        return jsonify({"error": "Type is required"}), 400
    with driver.session() as session:
        error = vehicle_access_error(session, vehicle_id)
        if error:
            return error
        record = session.run(
            f"MATCH (v:Vehicle {{id: $vehicle_id}}) SET {VEHICLE_FIELDS} RETURN v",
            vehicle_id=vehicle_id, **vehicle_params(data)
        ).single()
    return jsonify(vehicle_json(record["v"]))


@resource_bp.route('/vehicles/<vehicle_id>', methods=['DELETE'])
@jwt_required()
def delete_vehicle(vehicle_id):
    with driver.session() as session:
        error = vehicle_access_error(session, vehicle_id)
        if error:
            return error
        session.run("MATCH (v:Vehicle {id: $id}) DETACH DELETE v", id=vehicle_id)
    return jsonify({"message": "Vehicle deleted successfully"})


@resource_bp.route('/couriers')
@jwt_required()
def get_couriers():
    with driver.session() as session:
        if get_user_role(session, get_jwt_identity()) != 'manager':
            return jsonify({"error": "Forbidden: Only managers can view the full list of couriers"}), 403
        result = session.run("MATCH (u:User {account_type: 'courier'}) RETURN u")
        couriers = [courier_json(r["u"]) for r in result]
    return jsonify({"couriers": couriers})


@resource_bp.route('/couriers', methods=['POST'])
def create_courier():
    data = request.get_json()
    if not data.get("id"):
        return jsonify({"error": "Courier ID is required"}), 400
    with driver.session() as session:
        session.run(
            "CREATE (u:User {id: $id, name: $name, surname: $surname, email: $email, phone_number: $phone_number, "
            "account_type: 'courier', is_active: $is_active, password: $password, motorcycle_license: $motorcycle_license, "
            "car_license: $car_license, salary: $salary, average_rating: $average_rating, is_available: false})",
            id=data["id"], name=data["name"], surname=data["surname"], email=data["email"],
            phone_number=data["phone_number"], is_active=data.get("is_active", True),
            password=data.get("password", "pass1234"), motorcycle_license=data.get("motorcycle_license", False),
            car_license=data.get("car_license", False), salary=data.get("salary", 0.0),
            average_rating=data.get("average_rating", 0.0)
        )
    return jsonify({"message": "Courier created successfully"}), 201


@resource_bp.route('/couriers/<courier_id>/update', methods=['PUT'])
@invalidate_cache("user")
def update_courier(courier_id):
    data = request.get_json()
    with driver.session() as session:
        record = session.run(
            "MATCH (u:User {id: $courier_id, account_type: 'courier'}) "
            "SET u.name = $name, u.surname = $surname, u.email = $email, u.phone_number = $phone_number, "
            "u.is_active = $is_active, u.motorcycle_license = $motorcycle_license, u.car_license = $car_license, "
            "u.salary = $salary, u.average_rating = $average_rating RETURN u",
            courier_id=courier_id, name=data["name"], surname=data["surname"], email=data["email"],
            phone_number=data["phone_number"], is_active=data["is_active"],
            motorcycle_license=data.get("motorcycle_license", False), car_license=data.get("car_license", False),
            salary=data.get("salary", 0.0), average_rating=data.get("average_rating", 0.0)
        ).single()
    if not record:
        return jsonify({"error": "Courier not found"}), 404
    return jsonify(courier_json(record["u"]))


@resource_bp.route('/couriers/<courier_id>', methods=['DELETE'])
@invalidate_cache("user")
def delete_courier(courier_id):
    with driver.session() as session:
        record = session.run(
            "MATCH (u:User {id: $id, account_type: 'courier'}) DETACH DELETE u RETURN COUNT(u) AS deleted_count",
            id=courier_id
        ).single()
    if record["deleted_count"] > 0:
        return jsonify({"message": "Courier deleted successfully"})
    return jsonify({"error": "Courier not found"}), 404


@resource_bp.route('/products')
def get_products():
    with driver.session() as session:
        products = [product_json(r["p"]) for r in session.run("MATCH (p:Product) RETURN p")]
    return jsonify({"products": products})


@resource_bp.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    if not data.get("id"):
        return jsonify({"error": "Product ID is required"}), 400
    with driver.session() as session:
        session.run(
            "CREATE (p:Product {id: $id, name: $name, description: $description, price: $price})",
            id=data["id"], name=data["name"], description=data["description"], price=data["price"]
        )
    return jsonify({"message": "Product created successfully"}), 201


@resource_bp.route('/products/<product_id>/update', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    with driver.session() as session:
        record = session.run(
            "MATCH (p:Product {id: $id}) SET p.name = $name, p.description = $description, p.price = $price RETURN p",
            id=product_id, name=data["name"], description=data["description"], price=data["price"]
        ).single()
    if not record:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product_json(record["p"]))


@resource_bp.route('/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    with driver.session() as session:
        record = session.run(
            "MATCH (p:Product {id: $id}) DETACH DELETE p RETURN COUNT(p) AS deleted_count", id=product_id
        ).single()
    if record["deleted_count"] > 0:
        return jsonify({"message": "Product deleted successfully"})
    return jsonify({"error": "Product not found"}), 404
