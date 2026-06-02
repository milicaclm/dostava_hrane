#servis za dostave
from flask import Flask, request, jsonify
import os
import requests
from redis import Redis
from neo4j import GraphDatabase
app = Flask(__name__)

driver = GraphDatabase.driver("bolt://neo4j:7687", auth=("neo4j", "password"))

redis_client = Redis(
    host=os.environ.get("REDIS_HOST", "localhost"),
    port=int(os.environ.get("REDIS_PORT", 6379)),
    decode_responses=True
)

# helper to stringify Neo4j DateTime objects for JSON
def _fmt_dt(v):
    if v is None:
        return None
    try:
        return str(v)
    except Exception:
        return None


@app.route('/')
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
    
@app.route('/<delivery_id>')
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

# -----------------------Pravljenje porudžbine-----------------------------------------
@app.route('/', methods=['POST'])
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

@app.route('/<delivery_id>', methods=['PUT'])
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
        

@app.route('/<delivery_id>', methods=['DELETE'])
def delete_delivery(delivery_id):
    with driver.session() as session:
        result = session.run("MATCH (d:Delivery {id: $delivery_id}) DETACH DELETE d RETURN COUNT(d) AS deleted_count", delivery_id=delivery_id)
        record = result.single()
        if record["deleted_count"] > 0:
            return jsonify({"message": "Delivery deleted successfully"})
        else:
            return jsonify({"error": "Delivery not found"}), 404
        

@app.route('/<delivery_id>/products', methods=['POST'])
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
        
@app.route('/<delivery_id>/products/<product_id>', methods=['DELETE'])
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
        
@app.route('/<delivery_id>/products', methods=['GET'])
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


@app.route('/<delivery_id>/placed_by/<customer_id>', methods=['POST'])
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


@app.route('/<delivery_id>/placed_by/<customer_id>', methods=['DELETE'])
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

#------------------------------------------------------------------------------------------

@app.route('/<delivery_id>/assign_courier/<courier_id>', methods=['POST'])
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


#TODO: Treba da bude kompleksna funkcionalnost!
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


@app.route('/<delivery_id>/courier', methods=['GET'])
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

@app.route('/<delivery_id>/vehicle', methods=['GET'])
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
        


    




@app.route('/deliveries/<delivery_id>/complete', methods=['POST'])
def complete_delivery(delivery_id):
    """Mark delivery delivered and record vehicle history (IstorijaVozila).
    Expects JSON: {"courier_id": "...", "license_plate": "...", "note": "optional"}
    """
    data = request.get_json(force=True)
    courier_id = data.get('courier_id')
    note = data.get('note')

    with driver.session() as session:
        # verify delivery
        if not session.run("MATCH (d:Delivery {id: $delivery_id}) RETURN d", delivery_id=delivery_id).single():
            return jsonify({"error": "Delivery not found"}), 404

        # set delivery status and delivered time (sample_data uses 'completed')
        session.run(
            "MATCH (d:Delivery {id: $delivery_id}) SET d.status = 'completed', d.time_delivered = datetime() RETURN d",
            delivery_id=delivery_id
        )
        # if courier is present, update Redis and stop tracking
        if courier_id:
            try:
                redis_client.hset(f"pos:{courier_id}", mapping={"delivery_status": "completed"})
            except Exception:
                import traceback
                traceback.print_exc()
            try:
                requests.post("http://location-service:8080/stop", json={"user_id": courier_id}, timeout=2)
            except Exception:
                import traceback
                traceback.print_exc()

        # vehicle history creation removed (license_plate not required)

    return jsonify({"status": "completed", "delivery_id": delivery_id}), 200


@app.route('/deliveries/<delivery_id>/history', methods=['GET'])
def get_delivery_history(delivery_id):
    with driver.session() as session:
        if not session.run("MATCH (d:Delivery {id: $delivery_id}) RETURN d", delivery_id=delivery_id).single():
            return jsonify({"error": "Delivery not found"}), 404

        result = session.run(
            "MATCH (h:IstorijaVozila)-[:FOR_DELIVERY]->(d:Delivery {id: $delivery_id})<-[:FOR_DELIVERY]-(h) RETURN h ORDER BY h.ts DESC",
            delivery_id=delivery_id
        )
        history = []
        for record in result:
            h = record['h']
            history.append({
                'vozilo_id': h.get('vozilo_id'),
                'dostavljac_id': h.get('dostavljac_id'),
                'dostava_id': h.get('dostava_id'),
                'note': h.get('note'),
                'ts': str(h.get('ts'))
            })
    return jsonify({'history': history})


# --- Offer / suggestion workflow ---
@app.route('/deliveries/<delivery_id>/propose_couriers', methods=['GET'])
def propose_couriers(delivery_id):
    """Return candidate couriers for a delivery (simple heuristic).
    Currently returns couriers with account_type 'courier' who are active and not currently assigned.
    """
    with driver.session() as session:
        # ensure delivery exists
        if not session.run("MATCH (d:Delivery {id: $delivery_id}) RETURN d", delivery_id=delivery_id).single():
            return jsonify({"error": "Delivery not found"}), 404

        result = session.run(
            "MATCH (u:User) WHERE u.account_type IN ['courier','delivery'] AND COALESCE(u.aktivan, true)=true "
            "AND NOT (u)-[:ASSIGNED_TO]->(:Delivery) RETURN u LIMIT 5"
        )
        candidates = []
        for r in result:
            u = r['u']
            candidates.append({
                'id': u.get('id'),
                'name': u.get('name'),
                'surname': u.get('surname'),
                'phone_number': u.get('phone_number')
            })
    return jsonify({'candidates': candidates})


@app.route('/deliveries/<delivery_id>/offer/<courier_id>', methods=['POST'])
def offer_delivery_to_courier(delivery_id, courier_id):
    """Create an OFFER relationship from system to courier for this delivery."""
    with driver.session() as session:
        if not session.run("MATCH (d:Delivery {id: $delivery_id}) RETURN d", delivery_id=delivery_id).single():
            return jsonify({"error": "Delivery not found"}), 404
        if not session.run("MATCH (u:User {id: $courier_id}) RETURN u", courier_id=courier_id).single():
            return jsonify({"error": "Courier not found"}), 404

        # idempotent offer
        session.run(
            "MATCH (u:User {id: $courier_id}), (d:Delivery {id: $delivery_id}) MERGE (u)-[r:OFFERED]->(d) SET r.ts = datetime(), r.status='offered'",
            courier_id=courier_id,
            delivery_id=delivery_id
        )
    return jsonify({'message': 'Offer created'}), 201


@app.route('/deliveries/<delivery_id>/accept', methods=['POST'])
def accept_offer(delivery_id):
    data = request.get_json(force=True)
    user_id = data.get('user_id') or data.get('courier_id')
    if not user_id:
        return jsonify({'error': 'user_id required'}), 400

    with driver.session() as session:
        if not session.run("MATCH (d:Delivery {id: $delivery_id}) RETURN d", delivery_id=delivery_id).single():
            return jsonify({'error': 'Delivery not found'}), 404

        if not session.run("MATCH (u:User {id: $user_id}) RETURN u", user_id=user_id).single():
            return jsonify({'error': 'Courier not found'}), 404

        assigned_record = session.run(
            "MATCH (u:User)-[r:ASSIGNED_TO]->(d:Delivery {id: $delivery_id}) RETURN u.id AS assigned_id LIMIT 1",
            delivery_id=delivery_id
        ).single()
        if assigned_record:
            if assigned_record['assigned_id'] == user_id:
                return jsonify({'message': 'Delivery already assigned to this courier'}), 200
            return jsonify({'error': 'Delivery already assigned to another courier'}), 409

        offered = session.run(
            "MATCH (u:User {id: $user_id})-[r:OFFERED]->(d:Delivery {id: $delivery_id}) RETURN r",
            user_id=user_id,
            delivery_id=delivery_id
        ).single()

        session.run(
            "MATCH (u:User {id: $user_id}), (d:Delivery {id: $delivery_id}) MERGE (u)-[:ASSIGNED_TO]->(d) SET d.status='accepted'",
            user_id=user_id,
            delivery_id=delivery_id
        )
        if offered:
            session.run(
                "MATCH (u:User {id: $user_id})-[r:OFFERED]->(d:Delivery {id: $delivery_id}) DELETE r",
                user_id=user_id,
                delivery_id=delivery_id
            )

        try:
            redis_client.hset(f"pos:{user_id}", mapping={
                "delivery_id": delivery_id,
                "delivery_status": "accepted"
            })
        except Exception:
            import traceback
            traceback.print_exc()

        try:
            loc_payload = {"user_id": user_id, "delivery_id": delivery_id, "delivery_status": "accepted"}
            requests.post("http://location-service:8080/start", json=loc_payload, timeout=2)
        except Exception:
            import traceback
            traceback.print_exc()

    return jsonify({'message': 'Delivery accepted and assigned'}), 200


@app.route('/deliveries/<delivery_id>/reject', methods=['POST'])
def reject_offer(delivery_id):
    data = request.get_json(force=True)
    courier_id = data.get('courier_id')
    if not courier_id:
        return jsonify({'error': 'courier_id required'}), 400
    with driver.session() as session:
        session.run(
            "MATCH (u:User {id: $courier_id})-[r:OFFERED]->(d:Delivery {id: $delivery_id}) SET r.status='rejected'",
            courier_id=courier_id,
            delivery_id=delivery_id
        )
    return jsonify({'message': 'Offer rejected'}), 200


# Courier actions: pickup, deliver, cancel
@app.route('/deliveries/<delivery_id>/pickup', methods=['POST'])
def courier_pickup(delivery_id):
    data = request.get_json(force=True)
    courier_id = data.get('courier_id')
    if not courier_id:
        return jsonify({'error': 'courier_id required'}), 400
    with driver.session() as session:
        # verify assigned
        if not session.run("MATCH (u:User {id: $courier_id})-[:ASSIGNED_TO]->(d:Delivery {id: $delivery_id}) RETURN d", courier_id=courier_id, delivery_id=delivery_id).single():
            return jsonify({'error': 'Not assigned to this courier'}), 403
        session.run("MATCH (d:Delivery {id: $delivery_id}) SET d.status='in_transit', d.time_preuzimanja = datetime() RETURN d", delivery_id=delivery_id)
        # update Redis status so location-service writes it into points
        try:
            redis_client.hset(f"pos:{courier_id}", mapping={"delivery_status": "in_transit"})
        except Exception:
            import traceback
            traceback.print_exc()
    return jsonify({'message': 'Pickup recorded'}), 200


@app.route('/deliveries/<delivery_id>/deliver', methods=['POST'])
def courier_deliver(delivery_id):
    data = request.get_json(force=True)
    courier_id = data.get('courier_id')
    if not courier_id:
        return jsonify({'error': 'courier_id required'}), 400
    with driver.session() as session:
        if not session.run("MATCH (u:User {id: $courier_id})-[:ASSIGNED_TO]->(d:Delivery {id: $delivery_id}) RETURN d", courier_id=courier_id, delivery_id=delivery_id).single():
            return jsonify({'error': 'Not assigned to this courier'}), 403
        # mark delivered (sample_data uses 'completed')
        session.run("MATCH (d:Delivery {id: $delivery_id}) SET d.status='completed', d.time_dostavljanja = datetime() RETURN d", delivery_id=delivery_id)
        # update Redis and stop tracking
        try:
            redis_client.hset(f"pos:{courier_id}", mapping={"delivery_status": "completed"})
        except Exception:
            import traceback
            traceback.print_exc()
        try:
            requests.post("http://location-service:8080/stop", json={"user_id": courier_id}, timeout=2)
        except Exception:
            import traceback
            traceback.print_exc()
        # optional: history creation removed (license_plate not required)
    return jsonify({'message': 'Delivery marked as completed'}), 200


@app.route('/deliveries/<delivery_id>/cancel', methods=['POST'])
def courier_cancel(delivery_id):
    data = request.get_json(force=True)
    courier_id = data.get('courier_id')
    with driver.session() as session:
        # allow cancelled by assigned courier
        assigned = session.run("MATCH (u:User {id: $courier_id})-[:ASSIGNED_TO]->(d:Delivery {id: $delivery_id}) RETURN d", courier_id=courier_id, delivery_id=delivery_id).single()
        if not assigned:
            return jsonify({'error': 'Not assigned to this courier'}), 403
        session.run("MATCH (d:Delivery {id: $delivery_id}) SET d.status='cancelled' RETURN d", delivery_id=delivery_id)
        # update Redis and stop tracking
        try:
            redis_client.hset(f"pos:{courier_id}", mapping={"delivery_status": "cancelled"})
        except Exception:
            import traceback
            traceback.print_exc()
        try:
            requests.post("http://location-service:8080/stop", json={"user_id": courier_id}, timeout=2)
        except Exception:
            import traceback
            traceback.print_exc()
        # remove assignment
        session.run("MATCH (u:User {id: $courier_id})-[r:ASSIGNED_TO]->(d:Delivery {id: $delivery_id}) DELETE r", courier_id=courier_id, delivery_id=delivery_id)
    return jsonify({'message': 'Delivery cancelled by courier'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)