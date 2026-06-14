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
        result = session.run(
            """
            MATCH (v:Vehicle)
            OPTIONAL MATCH (v)<-[:USES_VEHICLE]-(u:User)-[:ASSIGNED_TO]->(d:Delivery)
            WHERE d.status IN ['accepted', 'in_transit']
            WITH v, count(d) > 0 AS is_in_use
            RETURN v, is_in_use
            """
        )
        vehicles = []
        for record in result:
            vehicle_node = record["v"]
            is_in_use = record["is_in_use"]
            vehicles.append({
                "owner_id": vehicle_node.get("owner_id"),
                "type": vehicle_node["type"],
                "license_plate": vehicle_node["license_plate"],
                "is_ready": vehicle_node["is_ready"],
                "brand": vehicle_node.get("brand"),
                "model": vehicle_node.get("model"),
                "color": vehicle_node.get("color"),
                "in_use": is_in_use,
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
                "is_active": user_node["is_active"],
                "motorcycle_license": user_node.get("motorcycle_license", False),
                "car_license": user_node.get("car_license", False),
                "salary": user_node.get("salary", 0.0),
                "average_rating": user_node.get("average_rating", 0.0)
            })
    return {"couriers": couriers}

        
@resource_bp.route('/couriers/<courier_id>/update', methods=['PUT'])
def update_courier(courier_id):
    data = request.get_json()
    with driver.session() as session:
        result = session.run(
            "MATCH (u:User {id: $courier_id, account_type: 'courier'}) "
            "SET u.name = $name, u.surname = $surname, u.email = $email, u.phone_number = $phone_number, u.is_active = $is_active, "
            "u.motorcycle_license = $motorcycle_license, u.car_license = $car_license, u.salary = $salary, u.average_rating = $average_rating "
            "RETURN u",
            courier_id=courier_id,
            name=data["name"],
            surname=data["surname"],
            email=data["email"],
            phone_number=data["phone_number"],
            is_active=data["is_active"],
            motorcycle_license=data.get("motorcycle_license", False),
            car_license=data.get("car_license", False),
            salary=data.get("salary", 0.0),
            average_rating=data.get("average_rating", 0.0)
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
                "is_active": user_node["is_active"],
                "motorcycle_license": user_node.get("motorcycle_license", False),
                "car_license": user_node.get("car_license", False),
                "salary": user_node.get("salary", 0.0),
                "average_rating": user_node.get("average_rating", 0.0)
            }
            return jsonify(courier)
        else:
            return jsonify({"error": "Courier not found"}), 404
        
@resource_bp.route('/vehicles/<license_plate>/update', methods=['PUT'])
def update_vehicle(license_plate):
    data = request.get_json()
    with driver.session() as session:
        result = session.run(
            """
            MATCH (v:Vehicle {license_plate: $license_plate})
            SET v.owner_id = $owner_id, v.type = $type, v.is_ready = $is_ready, v.brand = $brand, v.model = $model,
            v.color = $color, v.description = $description
            WITH v
            OPTIONAL MATCH (v)<-[:USES_VEHICLE]-(u:User)-[:ASSIGNED_TO]->(d:Delivery)
            WHERE d.status IN ['accepted', 'in_transit']
            WITH v, count(d) > 0 AS is_in_use
            RETURN v, is_in_use
            """,
            license_plate=license_plate,
            owner_id=data.get("owner_id"),
            type=data["type"],
            is_ready=data["is_ready"],
            brand=data.get("brand"),
            model=data.get("model"),
            color=data.get("color"),
            description=data.get("description")
        )
        record = result.single()
        if record:
            vehicle_node = record["v"]
            is_in_use = record["is_in_use"]
            vehicle = {
                "owner_id": vehicle_node.get("owner_id"),
                "type": vehicle_node["type"],
                "license_plate": vehicle_node["license_plate"],
                "is_ready": vehicle_node["is_ready"],
                "brand": vehicle_node.get("brand"),
                "model": vehicle_node.get("model"),
                "color": vehicle_node.get("color"),
                "in_use": is_in_use,
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
            """
            CREATE (v:Vehicle {owner_id: $owner_id, type: $type, license_plate: $license_plate, is_ready: $is_ready,
            brand: $brand, model: $model, color: $color, description: $description})
            """,
            owner_id=data.get("owner_id"),
            type=data["type"],
            license_plate=data["license_plate"],
            is_ready=data["is_ready"],
            brand=data.get("brand"),
            model=data.get("model"),
            color=data.get("color"),
            description=data.get("description")
        )
    return jsonify({"message": "Vehicle created successfully"}), 201

@resource_bp.route('/couriers', methods=['POST'])
def create_courier():
    data = request.get_json()
    with driver.session() as session:
        session.run(
            "CREATE (u:User {id: $id, name: $name, surname: $surname, email: $email, phone_number: $phone_number, account_type: 'courier', is_active: $is_active, password: $password, motorcycle_license: $motorcycle_license, car_license: $car_license, salary: $salary, average_rating: $average_rating})",
            id=data["id"],
            name=data["name"],
            surname=data["surname"],
            email=data["email"],
            phone_number=data["phone_number"],
            is_active=data.get("is_active", True),
            password=data.get("password", "pass1234"),
            motorcycle_license=data.get("motorcycle_license", False),
            car_license=data.get("car_license", False),
            salary=data.get("salary", 0.0),
            average_rating=data.get("average_rating", 0.0)
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
        
