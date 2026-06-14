#servis za menadžment resursima
import os
from flask import Blueprint, jsonify, request
from neo4j import GraphDatabase

resource_bp = Blueprint('resource', __name__)

driver = GraphDatabase.driver(
    os.environ.get("NEO4J_URI", "bolt://neo4j:7687"), 
    auth=(os.environ.get("NEO4J_USERNAME", "neo4j"), os.environ.get("NEO4J_PASSWORD", "password"))
)

@resource_bp.route('/')
def hello():
    return "Hello, Resource Service!"

@resource_bp.route('/vehicles')
def get_vehicles():
    with driver.session() as session:
        result = session.run("MATCH (v:Vehicle) RETURN v")
        vehicles = []
        for record in result:
            vehicle_node = record["v"]
            vehicles.append({
                "type": vehicle_node["type"],
                "license_plate": vehicle_node["license_plate"],
                "is_ready": vehicle_node["is_ready"],
                "brand": vehicle_node.get("brand"),
                "model": vehicle_node.get("model"),
                "color": vehicle_node.get("color"),
                "in_use": vehicle_node.get("in_use"),
                "description": vehicle_node.get("description")
            })
    return {"vehicles": vehicles}

@resource_bp.route('/products')
def get_products():
    with driver.session() as session:
        result = session.run("MATCH (p:Product) RETURN p")
        products = []
        for record in result:
            product_node = record["p"]
            products.append({
                "id": product_node["id"],
                "name": product_node["name"],
                "description": product_node["description"],
                "price": product_node["price"]
            })
    return {"products": products}

@resource_bp.route('/couriers')
def get_couriers():
    with driver.session() as session:
        result = session.run("MATCH (u:User {account_type: 'courier'}) RETURN u")
        couriers = []
        for record in result:
            user_node = record["u"]
            couriers.append({
                "id": user_node["id"],
                "name": user_node["name"],
                "surname": user_node["surname"],
                "email": user_node["email"],
                "phone_number": user_node["phone_number"],
                "is_active": user_node["is_active"]
            })
    return {"couriers": couriers}

        
@resource_bp.route('/couriers/<courier_id>/update', methods=['PUT'])
def update_courier(courier_id):
    data = request.get_json()
    with driver.session() as session:
        result = session.run(
            "MATCH (u:User {id: $courier_id, account_type: 'courier'}) "
            "SET u.name = $name, u.surname = $surname, u.email = $email, u.phone_number = $phone_number, u.is_active = $is_active "
            "RETURN u",
            courier_id=courier_id,
            name=data["name"],
            surname=data["surname"],
            email=data["email"],
            phone_number=data["phone_number"],
            is_active=data["is_active"]
        )
        record = result.single()
        if record:
            user_node = record["u"]
            courier = {
                "id": user_node["id"],
                "name": user_node["name"],
                "surname": user_node["surname"],
                "email": user_node["email"],
                "phone_number": user_node["phone_number"],
                "is_active": user_node["is_active"]
            }
            return jsonify(courier)
        else:
            return jsonify({"error": "Courier not found"}), 404
        
@resource_bp.route('/vehicles/<license_plate>/update', methods=['PUT'])
def update_vehicle(license_plate):
    data = request.get_json()
    with driver.session() as session:
        result = session.run(
            "MATCH (v:Vehicle {license_plate: $license_plate}) "
            "SET v.type = $type, v.is_ready = $is_ready, v.brand = $brand, v.model = $model, "
            "v.color = $color, v.in_use = $in_use, v.description = $description "
            "RETURN v",
            license_plate=license_plate,
            type=data["type"],
            is_ready=data["is_ready"],
            brand=data.get("brand"),
            model=data.get("model"),
            color=data.get("color"),
            in_use=data.get("in_use"),
            description=data.get("description")
        )
        record = result.single()
        if record:
            vehicle_node = record["v"]
            vehicle = {
                "type": vehicle_node["type"],
                "license_plate": vehicle_node["license_plate"],
                "is_ready": vehicle_node["is_ready"],
                "brand": vehicle_node.get("brand"),
                "model": vehicle_node.get("model"),
                "color": vehicle_node.get("color"),
                "in_use": vehicle_node.get("in_use"),
                "description": vehicle_node.get("description")
            }
            return jsonify(vehicle)
        else:
            return jsonify({"error": "Vehicle not found"}), 404
        
@resource_bp.route('/products/<product_id>/update', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    with driver.session() as session:
        result = session.run(
            "MATCH (p:Product {id: $product_id}) "
            "SET p.name = $name, p.description = $description, p.price = $price "
            "RETURN p",
            product_id=product_id,
            name=data["name"],
            description=data["description"],
            price=data["price"]
        )
        record = result.single()
        if record:
            product_node = record["p"]
            product = {
                "id": product_node["id"],
                "name": product_node["name"],
                "description": product_node["description"],
                "price": product_node["price"]
            }
            return jsonify(product)
        else:
            return jsonify({"error": "Product not found"}), 404
        
# create

@resource_bp.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    with driver.session() as session:
        session.run(
            "CREATE (p:Product {id: $id, name: $name, description: $description, price: $price})",
            id=data["id"],
            name=data["name"],
            description=data["description"],
            price=data["price"]
        )
    return jsonify({"message": "Product created successfully"}), 201

@resource_bp.route('/vehicles', methods=['POST'])
def create_vehicle():
    data = request.get_json()
    with driver.session() as session:
        session.run(
            "CREATE (v:Vehicle {type: $type, license_plate: $license_plate, is_ready: $is_ready, "
            "brand: $brand, model: $model, color: $color, in_use: $in_use, description: $description})",
            type=data["type"],
            license_plate=data["license_plate"],
            is_ready=data["is_ready"],
            brand=data.get("brand"),
            model=data.get("model"),
            color=data.get("color"),
            in_use=data.get("in_use", False),
            description=data.get("description")
        )
    return jsonify({"message": "Vehicle created successfully"}), 201

@resource_bp.route('/couriers', methods=['POST'])
def create_courier():
    data = request.get_json()
    with driver.session() as session:
        session.run(
            "CREATE (u:User {id: $id, name: $name, surname: $surname, email: $email, phone_number: $phone_number, account_type: 'courier', is_active: $is_active, password: $password})",
            id=data["id"],
            name=data["name"],
            surname=data["surname"],
            email=data["email"],
            phone_number=data["phone_number"],
            is_active=data["is_active"],
            password=data["password"]
        )
    return jsonify({"message": "Courier created successfully"}), 201

# delete

@resource_bp.route('/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    with driver.session() as session:
        result = session.run(
            "MATCH (p:Product {id: $product_id}) DETACH DELETE p RETURN COUNT(p) AS deleted_count",
            product_id=product_id
        )
        record = result.single()
        if record["deleted_count"] > 0:
            return jsonify({"message": "Product deleted successfully"})
        else:
            return jsonify({"error": "Product not found"}), 404
    
@resource_bp.route('/vehicles/<license_plate>', methods=['DELETE'])
def delete_vehicle(license_plate):
    with driver.session() as session:
        result = session.run(
            "MATCH (v:Vehicle {license_plate: $license_plate}) DETACH DELETE v RETURN COUNT(v) AS deleted_count",
            license_plate=license_plate
        )
        record = result.single()
        if record["deleted_count"] > 0:
            return jsonify({"message": "Vehicle deleted successfully"})
        else:
            return jsonify({"error": "Vehicle not found"}), 404
    
@resource_bp.route('/couriers/<courier_id>', methods=['DELETE'])
def delete_courier(courier_id):
    with driver.session() as session:
        result = session.run(
            "MATCH (u:User {id: $courier_id, account_type: 'courier'}) DETACH DELETE u RETURN COUNT(u) AS deleted_count",
            courier_id=courier_id
        )
        record = result.single()
        if record["deleted_count"] > 0:
            return jsonify({"message": "Courier deleted successfully"})
        else:
            return jsonify({"error": "Courier not found"}), 404
        
