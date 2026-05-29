#servis za dostave
from flask import Flask, request, jsonify
from neo4j import GraphDatabase
app = Flask(__name__)



driver = GraphDatabase.driver("bolt://neo4j:7687", auth=("neo4j", "password"))

# helper to stringify Neo4j DateTime objects for JSON
def _fmt_dt(v):
    if v is None:
        return None
    try:
        return str(v)
    except Exception:
        return None

@app.route('/')
def hello():
    return "Hello, Delivery Service!"

@app.route('/deliveries')
def get_deliveries():
    with driver.session() as session:
        result = session.run("MATCH (d:Delivery) RETURN d")
        deliveries = []
        for record in result:
            delivery_node = record["d"]
            deliveries.append({
                "id": delivery_node["id"],
                "status": delivery_node["status"],
                "from_location": delivery_node["from_location"],
                "to_location": delivery_node["to_location"],
                "order_time": _fmt_dt(delivery_node.get("order_time"))
            })
    return jsonify(deliveries)
    
@app.route('/deliveries/<delivery_id>')
def get_delivery(delivery_id):
    with driver.session() as session:
        result = session.run("MATCH (d:Delivery {id: $delivery_id}) RETURN d", delivery_id=delivery_id)
        record = result.single()
        if record:
            delivery_node = record["d"]
            delivery = {
                "id": delivery_node["id"],
                "status": delivery_node["status"],
                "from_location": delivery_node["from_location"],
                "to_location": delivery_node["to_location"],
                "order_time": _fmt_dt(delivery_node.get("order_time"))
            }
            return jsonify(delivery)
        else:
            return jsonify({"error": "Delivery not found"}), 404

@app.route('/deliveries', methods=['POST'])
def create_delivery():
    data = request.get_json()
    with driver.session() as session:
        session.run(
            "CREATE (d:Delivery {id: $id, status: $status, from_location: $from_location, to_location: $to_location, order_time: $order_time})",
            id=data["id"],
            status=data["status"],
            from_location=data["from_location"],
            to_location=data["to_location"],
            order_time=data["order_time"]
        )
    return jsonify({"message": "Delivery created successfully"}), 201

@app.route('/deliveries/<delivery_id>', methods=['PUT'])
def update_delivery(delivery_id):
    data = request.get_json()
    with driver.session() as session:
        result = session.run(
            "MATCH (d:Delivery {id: $delivery_id}) "
            "SET d.status = $status, d.from_location = $from_location, d.to_location = $to_location, d.order_time = $order_time "
            "RETURN d",
            delivery_id=delivery_id,
            status=data["status"],
            from_location=data["from_location"],
            to_location=data["to_location"],
            order_time=data["order_time"]
        )
        record = result.single()
        if record:
            delivery_node = record["d"]
            delivery = {
                "id": delivery_node["id"],
                "status": delivery_node["status"],
                "from_location": delivery_node["from_location"],
                "to_location": delivery_node["to_location"],
                "order_time": _fmt_dt(delivery_node.get("order_time"))
            }
            return jsonify(delivery)
        else:
            return jsonify({"error": "Delivery not found"}), 404
        

@app.route('/deliveries/<delivery_id>', methods=['DELETE'])
def delete_delivery(delivery_id):
    with driver.session() as session:
        result = session.run("MATCH (d:Delivery {id: $delivery_id}) DETACH DELETE d RETURN COUNT(d) AS deleted_count", delivery_id=delivery_id)
        record = result.single()
        if record["deleted_count"] > 0:
            return jsonify({"message": "Delivery deleted successfully"})
        else:
            return jsonify({"error": "Delivery not found"}), 404


@app.route('/deliveries/<delivery_id>/assign_courier/<courier_id>', methods=['POST'])
def assign_courier(delivery_id, courier_id):
    with driver.session() as session:

        if not session.run("MATCH (d:Delivery {id: $delivery_id}) RETURN d", delivery_id=delivery_id).single():
            return jsonify({"error": "Delivery not found"}), 404

        courier_rec = session.run(
            "MATCH (c:User {id: $courier_id}) WHERE c.account_type IN ['courier','delivery'] RETURN c",
            courier_id=courier_id
        ).single()
        if not courier_rec:
            return jsonify({"error": "Courier not found or invalid account_type"}), 404

        cnt = session.run(
            "MATCH (c:User {id: $courier_id})-[r:ASSIGNED_TO]->(d:Delivery {id: $delivery_id}) RETURN count(r) AS cnt",
            courier_id=courier_id,
            delivery_id=delivery_id
        ).single()["cnt"]
        if cnt > 0:
            return jsonify({"message": "Courier already assigned to this delivery"})

        other = session.run(
            "MATCH (other:User)-[r:ASSIGNED_TO]->(d:Delivery {id: $delivery_id}) RETURN other.id AS other_id LIMIT 1",
            delivery_id=delivery_id
        ).single()
        if other and other.get("other_id") and other.get("other_id") != courier_id:
            return jsonify({"error": "Delivery already assigned to another courier"}), 409
        
        res = session.run(
            "MATCH (c:User {id: $courier_id}), (d:Delivery {id: $delivery_id}) CREATE (c)-[:ASSIGNED_TO]->(d) RETURN c, d",
            courier_id=courier_id,
            delivery_id=delivery_id
        ).single()
        if res:
            c = res["c"]
            d = res["d"]
            return jsonify({"message": "Courier assigned", "courier": {"id": c.get("id")}, "delivery": {"id": d.get("id")}})
        return jsonify({"error": "Could not assign courier"}), 500

@app.route('/users/<user_id>/assign_vehicle/<license_plate>', methods=['POST'])
def assign_vehicle(user_id, license_plate):
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

    
    
        
@app.route('/deliveries/<delivery_id>/products', methods=['POST'])
def add_product_to_delivery(delivery_id):
    data = request.get_json()
    product_id = data["product_id"]
    with driver.session() as session:
        result = session.run(
            "MATCH (d:Delivery {id: $delivery_id}), (p:Product {id: $product_id}) "
            "CREATE (d)-[:CONTAINS_PRODUCT]->(p) RETURN d, p",
            delivery_id=delivery_id,
            product_id=product_id
        )
        record = result.single()
        if record:
            delivery_node = record["d"]
            product_node = record["p"]
            response = {
                "delivery": {
                    "id": delivery_node["id"],
                    "status": delivery_node["status"],
                    "from_location": delivery_node["from_location"],
                    "to_location": delivery_node["to_location"],
                    "order_time": _fmt_dt(delivery_node.get("order_time"))
                },
                "product": {
                    "id": product_node["id"],
                    "name": product_node["name"],
                    "description": product_node["description"],
                    "price": product_node["price"]
                }
            }
            return jsonify(response)
        else:
            return jsonify({"error": "Delivery or Product not found"}), 404
        
@app.route('/deliveries/<delivery_id>/products/<product_id>', methods=['DELETE'])
def remove_product_from_delivery(delivery_id, product_id):
    with driver.session() as session:
        result = session.run(
            "MATCH (d:Delivery {id: $delivery_id})-[r:CONTAINS_PRODUCT]->(p:Product {id: $product_id}) "
            "DELETE r RETURN COUNT(r) AS deleted_count",
            delivery_id=delivery_id,
            product_id=product_id
        )
        record = result.single()
        if record["deleted_count"] > 0:
            return jsonify({"message": "Product removed from delivery successfully"})
        else:
            return jsonify({"error": "Delivery or Product not found"}), 404

@app.route('/deliveries/<delivery_id>/courier', methods=['GET'])
def get_assigned_courier(delivery_id):
    with driver.session() as session:
        result = session.run(
            "MATCH (c:User)-[:ASSIGNED_TO]->(d:Delivery {id: $delivery_id}) "
            "RETURN c",
            delivery_id=delivery_id
        )
        record = result.single()
        if record:
            courier_node = record["c"]
            courier = {
                "id": courier_node["id"],
                "name": courier_node["name"],
                "surname": courier_node["surname"],
                "email": courier_node["email"],
                "phone_number": courier_node["phone_number"],
                "account_type": courier_node["account_type"],
            }
            return jsonify({"courier": courier})
        else:
            return jsonify({"error": "Assigned courier not found"}), 404

@app.route('/deliveries/<delivery_id>/vehicle', methods=['GET'])
def get_assigned_vehicle(delivery_id):
    with driver.session() as session:
        result = session.run(
            "MATCH (v:Vehicle)-[:USES_VEHICLE]->(d:Delivery {id: $delivery_id}) "
            "RETURN v",
            delivery_id=delivery_id
        )
        record = result.single()
        if record:
            vehicle_node = record["v"]
            vehicle = {
                "type": vehicle_node["type"],
                "license_plate": vehicle_node["license_plate"],
                "is_ready": vehicle_node["is_ready"]
            }
            return jsonify({"vehicle": vehicle})
        else:
            return jsonify({"error": "Assigned vehicle not found"}), 404
        
@app.route('/deliveries/<delivery_id>/products', methods=['GET'])
def get_delivery_products(delivery_id):
    with driver.session() as session:
        result = session.run(
            "MATCH (d:Delivery {id: $delivery_id})-[:CONTAINS_PRODUCT]->(p:Product) "
            "RETURN p",
            delivery_id=delivery_id
        )
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


# --- PLACED_ORDER endpoints (customer -> delivery)
@app.route('/deliveries/<delivery_id>/placed_by/<customer_id>', methods=['POST'])
def create_placed_order(delivery_id, customer_id):
    with driver.session() as session:
        # verify delivery
        if not session.run("MATCH (d:Delivery {id: $delivery_id}) RETURN d", delivery_id=delivery_id).single():
            return jsonify({"error": "Delivery not found"}), 404
        # verify customer
        if not session.run("MATCH (c:User {id: $customer_id}) WHERE c.account_type = 'customer' RETURN c", customer_id=customer_id).single():
            return jsonify({"error": "Customer not found"}), 404
        # idempotent create
        res = session.run(
            "MATCH (c:User {id: $customer_id}), (d:Delivery {id: $delivery_id}) MERGE (c)-[r:PLACED_ORDER]->(d) RETURN count(r) AS cnt",
            customer_id=customer_id,
            delivery_id=delivery_id
        ).single()
        return jsonify({"message": "Placed order relation created"}), 201


@app.route('/customers/<customer_id>/deliveries')
def list_customer_deliveries(customer_id):
    with driver.session() as session:
        result = session.run(
            "MATCH (c:User {id: $customer_id})-[:PLACED_ORDER]->(d:Delivery) RETURN d",
            customer_id=customer_id
        )
        deliveries = []
        for record in result:
            d = record['d']
            deliveries.append({
                'id': d.get('id'),
                'status': d.get('status'),
                'from_location': d.get('from_location'),
                'to_location': d.get('to_location'),
                'order_time': _fmt_dt(d.get('order_time'))
            })
    return jsonify({"deliveries": deliveries})


@app.route('/deliveries/<delivery_id>/placed_by/<customer_id>', methods=['DELETE'])
def delete_placed_order(delivery_id, customer_id):
    with driver.session() as session:
        res = session.run(
            "MATCH (c:User {id: $customer_id})-[r:PLACED_ORDER]->(d:Delivery {id: $delivery_id}) DELETE r RETURN COUNT(r) AS cnt",
            customer_id=customer_id,
            delivery_id=delivery_id
        ).single()
        if res and res.get('cnt', 0) > 0:
            return jsonify({"message": "Placed order relation removed"})
        return jsonify({"error": "Placed order relation not found"}), 404


# --- Vehicle CRUD endpoints (centralized here)
@app.route('/vehicles')
def list_vehicles():
    with driver.session() as session:
        result = session.run("MATCH (v:Vehicle) RETURN v")
        vehicles = []
        for record in result:
            v = record['v']
            vehicles.append({
                'type': v.get('type'),
                'license_plate': v.get('license_plate'),
                'is_ready': v.get('is_ready')
            })
    return jsonify({"vehicles": vehicles})


@app.route('/vehicles', methods=['POST'])
def create_vehicle():
    data = request.get_json()
    if not data or 'license_plate' not in data:
        return jsonify({"error": "license_plate required"}), 400
    with driver.session() as session:
        session.run(
            "CREATE (v:Vehicle {type: $type, license_plate: $license_plate, is_ready: $is_ready})",
            type=data.get('type', 'unknown'),
            license_plate=data['license_plate'],
            is_ready=data.get('is_ready', True)
        )
    return jsonify({"message": "Vehicle created successfully"}), 201


@app.route('/vehicles/<license_plate>', methods=['PUT'])
def update_vehicle(license_plate):
    data = request.get_json()
    if not data:
        return jsonify({"error": "body required"}), 400
    with driver.session() as session:
        res = session.run(
            "MATCH (v:Vehicle {license_plate: $license_plate}) SET v.type = $type, v.is_ready = $is_ready RETURN v",
            license_plate=license_plate,
            type=data.get('type'),
            is_ready=data.get('is_ready')
        ).single()
        if res:
            v = res['v']
            return jsonify({
                'type': v.get('type'),
                'license_plate': v.get('license_plate'),
                'is_ready': v.get('is_ready')
            })
        return jsonify({"error": "Vehicle not found"}), 404


@app.route('/vehicles/<license_plate>', methods=['DELETE'])
def delete_vehicle(license_plate):
    with driver.session() as session:
        res = session.run(
            "MATCH (v:Vehicle {license_plate: $license_plate}) DETACH DELETE v RETURN COUNT(v) AS cnt",
            license_plate=license_plate
        ).single()
        if res and res.get('cnt', 0) > 0:
            return jsonify({"message": "Vehicle deleted successfully"})
        return jsonify({"error": "Vehicle not found"}), 404


        

#place the order
@app.route('/deliveries/<delivery_id>/place_order', methods=['POST'])
def place_order(delivery_id):
    with driver.session() as session:
        result = session.run(
            "MATCH (d:Delivery {id: $delivery_id}) "
            "SET d.status = 'placed' "
            "RETURN d",
            delivery_id=delivery_id
        )
        record = result.single()
        if record:
            delivery_node = record["d"]
            delivery = {
                "id": delivery_node["id"],
                "status": delivery_node["status"],
                "from_location": delivery_node["from_location"],
                "to_location": delivery_node["to_location"],
                "order_time": _fmt_dt(delivery_node.get("order_time"))
            }
            return jsonify(delivery)
        else:
            return jsonify({"error": "Delivery not found"}), 404
        

@app.route('/deliveries/<delivery_id>/delete_order', methods=['DELETE'])
def delete_order(delivery_id):
    with driver.session() as session:
        result = session.run(
            "MATCH (d:Delivery {id: $delivery_id}) "
            "DELETE d "
            "RETURN d",
            delivery_id=delivery_id
        )
        record = result.single()
        if record:
            return jsonify({"message": "Delivery deleted successfully"})
        else:
            return jsonify({"error": "Delivery not found"}), 404

@app.route('/deliveries/<delivery_id>/update_order', methods=['POST'])
def update_order(delivery_id):
    data = request.get_json()
    with driver.session() as session:
        result = session.run(
            "MATCH (d:Delivery {id: $delivery_id}) "
            "SET d.from_location = $from_location, d.to_location = $to_location, d.order_time = $order_time "
            "RETURN d",
            delivery_id=delivery_id,
            from_location=data["from_location"],
            to_location=data["to_location"],
            order_time=data["order_time"]
        )
        record = result.single()
        if record:
            delivery_node = record["d"]
            delivery = {
                "id": delivery_node["id"],
                "status": delivery_node["status"],
                "from_location": delivery_node["from_location"],
                "to_location": delivery_node["to_location"],
                "order_time": _fmt_dt(delivery_node.get("order_time"))
            }
            return jsonify(delivery)
        else:
            return jsonify({"error": "Delivery not found"}), 404
    
@app.route('/deliveries/<delivery_id>/show_order')
def show_order(delivery_id):
    with driver.session() as session:
        result = session.run(
            "MATCH (d:Delivery {id: $delivery_id}) "
            "RETURN d",
            delivery_id=delivery_id
        )
        record = result.single()
        if record:
            delivery_node = record["d"]
            delivery = {
                "id": delivery_node["id"],
                "status": delivery_node["status"],
                "from_location": delivery_node["from_location"],
                "to_location": delivery_node["to_location"],
                "order_time": _fmt_dt(delivery_node.get("order_time"))
            }
            return jsonify(delivery)
        else:
            return jsonify({"error": "Delivery not found"}), 404

#delete assigned to and uses vehicle
@app.route('/deliveries/<delivery_id>/unassign_courier', methods=['DELETE'])
def unassign_courier(delivery_id):
    with driver.session() as session:
        result = session.run(
            "MATCH (c:User)-[r:ASSIGNED_TO]->(d:Delivery {id: $delivery_id}) "
            "DELETE r RETURN COUNT(r) AS deleted_count",
            delivery_id=delivery_id
        )
        record = result.single()
        if record["deleted_count"] > 0:
            return jsonify({"message": "Courier unassigned from delivery successfully"})
        else:
            return jsonify({"error": "Assigned courier not found"}), 404

@app.route('/deliveries/<delivery_id>/unassign_vehicle', methods=['DELETE'])
def unassign_vehicle(delivery_id):
    with driver.session() as session:
        result = session.run(
            "MATCH (v:Vehicle)-[r:USES_VEHICLE]->(d:Delivery {id: $delivery_id}) "
            "DELETE r RETURN COUNT(r) AS deleted_count",
            delivery_id=delivery_id
        )
        record = result.single()
        if record["deleted_count"] > 0:
            return jsonify({"message": "Vehicle unassigned from delivery successfully"})
        else:
            return jsonify({"error": "Assigned vehicle not found"}), 404
        

@app.route('/deliveries/<delivery_id>/placed_by/<customer_id>', methods=['PUT'])
def update_placed_order(delivery_id, customer_id):
    data = request.get_json()
    with driver.session() as session:

        if not session.run("MATCH (d:Delivery {id: $delivery_id}) RETURN d", delivery_id=delivery_id).single():
            return jsonify({"error": "Delivery not found"}), 404

        if not session.run("MATCH (c:User {id: $customer_id}) WHERE c.account_type = 'customer' RETURN c", customer_id=customer_id).single():
            return jsonify({"error": "Customer not found"}), 404

        res = session.run(
            "MATCH (c:User {id: $customer_id})-[r:PLACED_ORDER]->(d:Delivery {id: $delivery_id}) "
            "SET r.some_property = $some_value "
            "RETURN count(r) AS cnt",
            customer_id=customer_id,
            delivery_id=delivery_id,
            some_value=data.get("some_property")
            ).single()
        if res and res.get("cnt", 0) > 0:
            return jsonify({"message": "Placed order relation updated"})
        return jsonify({"error": "Placed order relation not found"}), 404
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)