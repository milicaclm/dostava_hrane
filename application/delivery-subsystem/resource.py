#servis za menadžment resursima
import os
import uuid
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from neo4j import GraphDatabase

resource_bp = Blueprint('resource', __name__)

driver = GraphDatabase.driver(
    os.environ.get("NEO4J_URI", "bolt://neo4j:7687"), 
    auth=(os.environ.get("NEO4J_USERNAME", "neo4j"), os.environ.get("NEO4J_PASSWORD", "password"))
)

def get_user_role(session, user_id):
    result = session.run("MATCH (u:User {id: $user_id}) RETURN u.account_type AS role", user_id=user_id)
    record = result.single()
    return record["role"] if record else None

@resource_bp.route('/')
def hello():
    return "Hello, Resource Service!"

@resource_bp.route('/vehicles')
@jwt_required()
def get_vehicles():
    owner_id_filter = request.args.get('owner_id')

    with driver.session() as session:
        params = {}
        
        # Osnovni upit koji dohvata sva vozila
        query_base = "MATCH (v:Vehicle)"

        # Ako je prosleđen filter za vlasnika, modifikuj upit sa filtriranjem is_ready=true za dostavljače
        if owner_id_filter:
            query_base = """
            MATCH (v:Vehicle)
            WHERE (v.owner_id = $owner_id OR v.owner_id IS NULL)
            WITH v
            OPTIONAL MATCH (u:User {id: $owner_id})
            WHERE u.account_type IN ['courier', 'delivery']
            WITH v, u
            WHERE u IS NULL OR v.is_ready = true
            """
            params['owner_id'] = owner_id_filter
        
        # Nastavak upita za proveru da li je vozilo u upotrebi i ko ga koristi
        query = f"""
        {query_base}
        OPTIONAL MATCH (v)<-[:USES_VEHICLE]-(u_assigned:User)
        WITH v, u_assigned.id AS assigned_user_id
        OPTIONAL MATCH (v)<-[:USES_VEHICLE]-(u:User)-[:ASSIGNED_TO]->(d:Delivery)
        WHERE d.status IN ['accepted', 'in_transit']
        WITH v, assigned_user_id, count(d) > 0 AS is_in_use
        RETURN v, assigned_user_id, is_in_use
        """
        
        result = session.run(query, params)
        vehicles = []
        for record in result:
            vehicle_node = record["v"]
            is_in_use = record["is_in_use"]
            assigned_user_id = record["assigned_user_id"]
            vehicles.append({
                "id": vehicle_node["id"],
                "owner_id": vehicle_node.get("owner_id"),
                "type": vehicle_node["type"],
                "license_plate": vehicle_node["license_plate"],
                "is_ready": vehicle_node["is_ready"],
                "brand": vehicle_node.get("brand"),
                "model": vehicle_node.get("model"),
                "color": vehicle_node.get("color"),
                "in_use": is_in_use,
                "assigned_user_id": assigned_user_id,
                "description": vehicle_node.get("description")
            })
    return jsonify({"vehicles": vehicles})

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
    return jsonify({"products": products})

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
    return jsonify({"couriers": couriers})

        
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
        
@resource_bp.route('/vehicles/<vehicle_id>/update', methods=['PUT'])
@jwt_required()
def update_vehicle(vehicle_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validacija
    if not data.get("type") or not data.get("license_plate"):
        return jsonify({"error": "Type and License Plate are required"}), 400

    with driver.session() as session:
        user_role = get_user_role(session, current_user_id)
        if not user_role:
            return jsonify({"error": "User role not found."}), 403

        check_result = session.run("MATCH (v:Vehicle {id: $vehicle_id}) RETURN v.owner_id AS owner_id", vehicle_id=vehicle_id)
        vehicle_record = check_result.single()

        if not vehicle_record:
            return jsonify({"error": "Vehicle not found"}), 404

        vehicle_owner_id = vehicle_record["owner_id"]

        # Check permissions
        is_owner = (vehicle_owner_id == current_user_id)
        is_manager_and_unowned = (user_role == 'manager' and vehicle_owner_id is None)

        if not is_owner and not is_manager_and_unowned:
            return jsonify({"error": "Forbidden"}), 403

        result = session.run(
            """
            MATCH (v:Vehicle {id: $vehicle_id})
            SET v.license_plate = $license_plate, v.type = $type, v.is_ready = $is_ready, v.brand = $brand, v.model = $model,
            v.color = $color, v.description = $description
            WITH v
            OPTIONAL MATCH (v)<-[:USES_VEHICLE]-(u:User)-[:ASSIGNED_TO]->(d:Delivery)
            WHERE d.status IN ['accepted', 'in_transit']
            WITH v, count(d) > 0 AS is_in_use
            RETURN v, is_in_use
            """,
            vehicle_id=vehicle_id,
            license_plate=data.get("license_plate"),
            type=data["type"].lower(),
            is_ready=data.get("is_ready", True),
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
                "id": vehicle_node.get("id"),
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
            return jsonify({"error": "Vehicle not found or update failed"}), 404
        
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
    product_id = data.get("id")
    if not product_id:
        return jsonify({"error": "Product ID is required"}), 400
    with driver.session() as session:
        session.run(
            "CREATE (p:Product {id: $id, name: $name, description: $description, price: $price})",
            id=product_id,
            name=data["name"],
            description=data["description"],
            price=data["price"]
        )
    return jsonify({"message": "Product created successfully"}), 201

@resource_bp.route('/couriers', methods=['POST'])
def create_courier():
    data = request.get_json()
    courier_id = data.get("id")
    if not courier_id:
        return jsonify({"error": "Courier ID is required"}), 400
    with driver.session() as session:
        session.run(
            "CREATE (u:User {id: $id, name: $name, surname: $surname, email: $email, phone_number: $phone_number, account_type: 'courier', is_active: $is_active, password: $password, motorcycle_license: $motorcycle_license, car_license: $car_license, salary: $salary, average_rating: $average_rating})",
            id=courier_id,
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

@resource_bp.route('/vehicles', methods=['POST'])
@jwt_required()
def create_vehicle():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    # Validacija
    if not data.get("type") or not data.get("license_plate"):
        return jsonify({"error": "Type and License Plate are required"}), 400
    
    vehicle_id = f"v-{uuid.uuid4().hex[:8]}"
    
    with driver.session() as session:
        user_role = get_user_role(session, current_user_id)
        if not user_role:
            return jsonify({"error": "User role not found."}), 403

        owner_id_param = data.get("owner_id")
        final_owner_id = None

        if owner_id_param == "me":
            final_owner_id = current_user_id
        elif owner_id_param is None:
            if user_role != 'manager':
                return jsonify({"error": "Forbidden: Only managers can create company vehicles without owner."}), 403
            final_owner_id = None
        else:
            return jsonify({"error": "Forbidden: Cannot create a vehicle for another user."}), 403

        session.run(
            """
            CREATE (v:Vehicle {id: $id, owner_id: $owner_id, type: $type, license_plate: $license_plate, is_ready: $is_ready,
            brand: $brand, model: $model, color: $color, description: $description})
            """,
            id=vehicle_id,
            owner_id=final_owner_id,
            type=data["type"].lower(),
            license_plate=data["license_plate"],
            is_ready=data.get("is_ready", True),
            brand=data.get("brand"),
            model=data.get("model"),
            color=data.get("color"),
            description=data.get("description")
        )
    return jsonify({"message": "Vehicle created successfully", "id": vehicle_id}), 201


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
    
@resource_bp.route('/vehicles/<vehicle_id>', methods=['DELETE'])
@jwt_required()
def delete_vehicle(vehicle_id):
    current_user_id = get_jwt_identity()
    with driver.session() as session:
        user_role = get_user_role(session, current_user_id)
        if not user_role:
            return jsonify({"error": "User role not found."}), 403

        check_result = session.run(
            "MATCH (v:Vehicle {id: $vehicle_id}) RETURN v.owner_id AS owner_id",
            vehicle_id=vehicle_id
        )
        vehicle_record = check_result.single()

        if not vehicle_record:
            return jsonify({"error": "Vehicle not found"}), 404

        vehicle_owner_id = vehicle_record["owner_id"]

        # Check permissions
        is_owner = (vehicle_owner_id == current_user_id)
        is_manager_and_unowned = (user_role == 'manager' and vehicle_owner_id is None)

        if not is_owner and not is_manager_and_unowned:
            return jsonify({"error": "Forbidden"}), 403

        result = session.run(
            "MATCH (v:Vehicle {id: $vehicle_id}) DETACH DELETE v RETURN COUNT(v) AS deleted_count",
            vehicle_id=vehicle_id
        )
        record = result.single()
        if record["deleted_count"] > 0:
            return jsonify({"message": "Vehicle deleted successfully"})
        else:
            return jsonify({"error": "Vehicle not found or deletion failed"}), 404
    
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