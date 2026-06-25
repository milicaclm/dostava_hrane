#servis za dostave
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
import requests
import math
import time
import threading
from redis import Redis
from neo4j import GraphDatabase
delivery_bp = Blueprint('delivery', __name__)

# In-memory store: { courier_id: {delivery_id, score, offered_at} }
# Represents the current batch of pending offers (not yet accepted/rejected)
_pending_offers: dict = {}

def get_user_role(session, user_id):
    result = session.run("MATCH (u:User {id: $user_id}) RETURN u.account_type AS role", user_id=user_id)
    record = result.single()
    return record["role"] if record else None

driver = GraphDatabase.driver(
    os.environ.get("NEO4J_URI", "bolt://neo4j:7687"), 
    auth=(os.environ.get("NEO4J_USERNAME", "neo4j"), os.environ.get("NEO4J_PASSWORD", "password"))
)

redis_client = Redis(
    host=os.environ.get("REDIS_HOST", "localhost"),
    port=int(os.environ.get("REDIS_PORT", 6379)),
    decode_responses=True
)

INTERNAL_API_URL = os.environ.get("INTERNAL_API_URL", "http://localhost:8080")

# helper to stringify Neo4j DateTime objects for JSON
def _fmt_dt(v):
    if v is None:
        return None
    try:
        return str(v)
    except Exception:
        return None


@delivery_bp.route('/')
@jwt_required()
def get_deliveries():
    current_user_id = get_jwt_identity()
    with driver.session() as session:
        user_role = get_user_role(session, current_user_id)
        if user_role != 'manager':
            return jsonify({"error": "Forbidden: Only managers can view the full list of deliveries"}), 403

        result = session.run(
            "MATCH (d:Delivery) "
            "OPTIONAL MATCH (u:User)-[r:OFFERED]->(d) "
            "WHERE r.status IN ['offered', 'pending', 'in transit', 'completed'] "
            "RETURN d, u, r.status AS status"
        )
        deliveries = []
        for record in result:
            delivery_node = record["d"]
            user_node = record["u"]
            status = record["status"] or "placed"
            
            courier_info = None
            if user_node:
                courier_info = f"{user_node['id']} - {user_node.get('name', '')} {user_node.get('surname', '')}".strip()

            deliveries.append({
                "id": delivery_node["id"],
                "status": status,
                "from_location": delivery_node["from_location"],
                "to_location": delivery_node["to_location"],
                "start_time": _fmt_dt(delivery_node.get("start_time")),
                "pickup_time": _fmt_dt(delivery_node.get("pickup_time")),
                "delivery_time": _fmt_dt(delivery_node.get("delivery_time")),
                "rating": delivery_node.get("rating"),
                "order_time": _fmt_dt(delivery_node.get("order_time")),
                "restaurant_lat": delivery_node.get("restaurant_lat"),
                "restaurant_lon": delivery_node.get("restaurant_lon"),
                "customer_lat": delivery_node.get("customer_lat"),
                "customer_lon": delivery_node.get("customer_lon"),
                "courier": courier_info
            })
    return jsonify(deliveries)
    
@delivery_bp.route('/<delivery_id>')
def get_delivery(delivery_id):
    with driver.session() as session:
        result = session.run(
            "MATCH (d:Delivery {id: $delivery_id}) "
            "OPTIONAL MATCH (u:User)-[r:OFFERED]->(d) "
            "WHERE r.status IN ['offered', 'pending', 'in transit', 'completed'] "
            "RETURN d, u, r.status AS status", 
            delivery_id=delivery_id
        )
        record = result.single()
        if record:
            delivery_node = record["d"]
            user_node = record["u"]
            status = record["status"] or "placed"
            courier_info = None
            if user_node:
                courier_info = f"{user_node['id']} - {user_node.get('name', '')} {user_node.get('surname', '')}".strip()
                
            delivery = {
                "id": delivery_node["id"],
                "status": status,
                "from_location": delivery_node["from_location"],
                "to_location": delivery_node["to_location"],
                "order_time": _fmt_dt(delivery_node.get("order_time")),
                "start_time": _fmt_dt(delivery_node.get("start_time")),
                "pickup_time": _fmt_dt(delivery_node.get("pickup_time")),
                "delivery_time": _fmt_dt(delivery_node.get("delivery_time")),
                "rating": delivery_node.get("rating"),
                "restaurant_lat": delivery_node.get("restaurant_lat"),
                "restaurant_lon": delivery_node.get("restaurant_lon"),
                "customer_lat": delivery_node.get("customer_lat"),
                "customer_lon": delivery_node.get("customer_lon"),
                "courier": courier_info
            }
            return jsonify(delivery)
        else:
            return jsonify({"error": "Delivery not found"}), 404

# -----------------------Pravljenje porudžbine-----------------------------------------
@delivery_bp.route('/', methods=['POST'])
def create_delivery():
    data = request.get_json()
    with driver.session() as session:
        session.run(
            "CREATE (d:Delivery {id: $id, from_location: $from_location, "
            "to_location: $to_location, order_time: datetime($order_time), "
            "start_time: datetime($start_time), rating: $rating, "
            "restaurant_lat: $restaurant_lat, restaurant_lon: $restaurant_lon, "
            "customer_lat: $customer_lat, customer_lon: $customer_lon})",
            id=data["id"],
            from_location=data["from_location"],
            to_location=data["to_location"],
            order_time=data["order_time"],
            start_time=data.get("start_time"),
            rating=data.get("rating", 0),
            restaurant_lat=float(data["restaurant_lat"]) if data.get("restaurant_lat") is not None else None,
            restaurant_lon=float(data["restaurant_lon"]) if data.get("restaurant_lon") is not None else None,
            customer_lat=float(data["customer_lat"]) if data.get("customer_lat") is not None else None,
            customer_lon=float(data["customer_lon"]) if data.get("customer_lon") is not None else None
        )
    return jsonify({"message": "Delivery created successfully"}), 201

@delivery_bp.route('/<delivery_id>', methods=['PUT'])
def update_delivery(delivery_id):
    data = request.get_json()
    with driver.session() as session:
        result = session.run(
            "MATCH (d:Delivery {id: $delivery_id}) "
            "SET d.from_location = $from_location, d.to_location = $to_location, "
            "d.rating = $rating, d.start_time = datetime($start_time), d.order_time = datetime($order_time), "
            "d.restaurant_lat = $restaurant_lat, d.restaurant_lon = $restaurant_lon, "
            "d.customer_lat = $customer_lat, d.customer_lon = $customer_lon "
            "RETURN d",
            delivery_id=delivery_id,
            from_location=data["from_location"],
            to_location=data["to_location"],
            order_time=data.get("order_time"),
            rating=data.get("rating"),
            start_time=data.get("start_time"),
            restaurant_lat=float(data["restaurant_lat"]) if data.get("restaurant_lat") is not None else None,
            restaurant_lon=float(data["restaurant_lon"]) if data.get("restaurant_lon") is not None else None,
            customer_lat=float(data["customer_lat"]) if data.get("customer_lat") is not None else None,
            customer_lon=float(data["customer_lon"]) if data.get("customer_lon") is not None else None
        )
        record = result.single()
        if record:
            delivery_node = record["d"]
            
            # Dobavljanje statusa iz aktivne OFFERED veze
            status_res = session.run(
                "MATCH (d:Delivery {id: $delivery_id}) "
                "OPTIONAL MATCH (u:User)-[r:OFFERED]->(d) "
                "WHERE r.status IN ['offered', 'pending', 'in transit', 'completed'] "
                "RETURN r.status AS status",
                delivery_id=delivery_id
            ).single()
            status = (status_res["status"] if status_res else None) or "placed"

            delivery = {
                "id": delivery_node["id"],
                "status": status,
                "from_location": delivery_node["from_location"],
                "to_location": delivery_node["to_location"],
                "order_time": _fmt_dt(delivery_node.get("order_time")),
                "start_time": _fmt_dt(delivery_node.get("start_time")),
                "pickup_time": _fmt_dt(delivery_node.get("pickup_time")),
                "delivery_time": _fmt_dt(delivery_node.get("delivery_time")),
                "rating": delivery_node.get("rating"),
                "restaurant_lat": delivery_node.get("restaurant_lat"),
                "restaurant_lon": delivery_node.get("restaurant_lon"),
                "customer_lat": delivery_node.get("customer_lat"),
                "customer_lon": delivery_node.get("customer_lon")
            }
            return jsonify(delivery)
        else:
            return jsonify({"error": "Delivery not found"}), 404
        

@delivery_bp.route('/<delivery_id>', methods=['DELETE'])
def delete_delivery(delivery_id):
    with driver.session() as session:
        result = session.run("MATCH (d:Delivery {id: $delivery_id}) DETACH DELETE d RETURN COUNT(d) AS deleted_count", delivery_id=delivery_id)
        record = result.single()
        if record["deleted_count"] > 0:
            return jsonify({"message": "Delivery deleted successfully"})
        else:
            return jsonify({"error": "Delivery not found"}), 404
        

@delivery_bp.route('/<delivery_id>/products', methods=['POST'])
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
        
@delivery_bp.route('/<delivery_id>/products/<product_id>', methods=['DELETE'])
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
        
@delivery_bp.route('/<delivery_id>/products', methods=['GET'])
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


@delivery_bp.route('/<delivery_id>/placed_by/<customer_id>', methods=['POST'])
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





@delivery_bp.route('/<delivery_id>/placed_by/<customer_id>', methods=['DELETE'])
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
    

@delivery_bp.route('/<delivery_id>/placed_by/<customer_id>', methods=['PUT'])
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

@delivery_bp.route('/<delivery_id>/assign_courier/<courier_id>', methods=['POST'])
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
            "MATCH (c:User {id: $courier_id})-[r:OFFERED]->(d:Delivery {id: $delivery_id}) "
            "WHERE r.status IN ['offered', 'pending', 'in transit', 'completed'] "
            "RETURN count(r) AS cnt",
            courier_id=courier_id,
            delivery_id=delivery_id
        ).single()["cnt"]
        if cnt > 0:
            return jsonify({"message": "Courier already assigned/offered to this delivery"})

        other = session.run(
            "MATCH (other:User)-[r:OFFERED]->(d:Delivery {id: $delivery_id}) "
            "WHERE r.status IN ['offered', 'pending', 'in transit', 'completed'] "
            "RETURN other.id AS other_id LIMIT 1",
            delivery_id=delivery_id
        ).single()
        if other and other.get("other_id") and other.get("other_id") != courier_id:
            return jsonify({"error": "Delivery already assigned/offered to another courier"}), 409
        
        res = session.run(
            "MATCH (c:User {id: $courier_id}), (d:Delivery {id: $delivery_id}) "
            "MERGE (c)-[r:OFFERED]->(d) "
            "SET r.status = 'pending', r.ts = datetime() "
            "RETURN c, d",
            courier_id=courier_id,
            delivery_id=delivery_id
        ).single()
        if res:
            c = res["c"]
            d = res["d"]
            return jsonify({"message": "Courier assigned", "courier": {"id": c.get("id")}, "delivery": {"id": d.get("id")}})
        return jsonify({"error": "Could not assign courier"}), 500


@delivery_bp.route('/<delivery_id>/courier', methods=['GET'])
def get_assigned_courier(delivery_id):
    with driver.session() as session:
        result = session.run(
            "MATCH (c:User)-[r:OFFERED]->(d:Delivery {id: $delivery_id}) "
            "WHERE r.status IN ['pending', 'in transit', 'completed'] "
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
                "email": courier_node.get("email"),
                "phone_number": courier_node.get("phone_number"),
                "account_type": courier_node.get("account_type"),
            }
            return jsonify({"courier": courier})
        else:
            return jsonify({"error": "Assigned courier not found"}), 404

@delivery_bp.route('/<delivery_id>/vehicle', methods=['GET'])
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


@delivery_bp.route('/<delivery_id>/unassign_courier', methods=['DELETE'])
def unassign_courier(delivery_id):
    with driver.session() as session:
        result = session.run(
            "MATCH (c:User)-[r:OFFERED]->(d:Delivery {id: $delivery_id}) "
            "DELETE r RETURN COUNT(r) AS deleted_count",
            delivery_id=delivery_id
        )
        record = result.single()
        if record["deleted_count"] > 0:
            return jsonify({"message": "Courier unassigned from delivery successfully"})
        else:
            return jsonify({"error": "Assigned courier not found"}), 404

@delivery_bp.route('/<delivery_id>/unassign_vehicle', methods=['DELETE'])
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
        


    




@delivery_bp.route('/<delivery_id>/complete', methods=['POST'])
def complete_delivery(delivery_id):
    """Mark delivery delivered.
    Expects JSON: {"courier_id": "...", "note": "optional"}
    """
    data = request.get_json(force=True)
    courier_id = data.get('courier_id')

    with driver.session() as session:
        # verify delivery
        if not session.run("MATCH (d:Delivery {id: $delivery_id}) RETURN d", delivery_id=delivery_id).single():
            return jsonify({"error": "Delivery not found"}), 404

        # set relation status to completed
        session.run(
            "MATCH (u:User)-[r:OFFERED]->(d:Delivery {id: $delivery_id}) "
            "WHERE r.status IN ['pending', 'accepted', 'in transit'] "
            "SET r.status = 'completed', d.delivery_time = datetime()",
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
                # Sada je putanja /locations/stop jer je location_bp registrovan na /locations
                requests.post(f"{INTERNAL_API_URL}/locations/stop", json={"user_id": courier_id}, timeout=2)
            except Exception:
                import traceback
                traceback.print_exc()

    return jsonify({"status": "completed", "delivery_id": delivery_id}), 200

# --- Offer / suggestion workflow ---
@delivery_bp.route('/<delivery_id>/propose_couriers', methods=['GET'])
def propose_couriers(delivery_id):
    """Return candidate couriers for a delivery (simple heuristic).
    Currently returns couriers with account_type 'courier' who are active and not currently assigned.
    """
    with driver.session() as session:
        # ensure delivery exists
        if not session.run("MATCH (d:Delivery {id: $delivery_id}) RETURN d", delivery_id=delivery_id).single():
            return jsonify({"error": "Delivery not found"}), 404

        result = session.run(
            "MATCH (u:User) WHERE u.account_type IN ['courier','delivery'] AND COALESCE(u.is_active, true)=true "
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


@delivery_bp.route('/offers', methods=['GET'])
@jwt_required()
def get_offered_deliveries():
    """Return the current in-memory offer for this courier (if any)."""
    courier_id = get_jwt_identity()
    offer = _pending_offers.get(courier_id)
    if not offer:
        return jsonify([]), 200

    delivery_id = offer["delivery_id"]
    with driver.session() as session:
        result = session.run(
            "MATCH (d:Delivery {id: $delivery_id}) RETURN d",
            delivery_id=delivery_id
        ).single()
        if not result:
            # Delivery no longer exists – clean up stale offer
            _pending_offers.pop(courier_id, None)
            return jsonify([]), 200
        d = result["d"]
        return jsonify([{
            "id": d.get("id"),
            "status": "pending",
            "from_location": d.get("from_location"),
            "to_location": d.get("to_location"),
            "order_time": _fmt_dt(d.get("order_time")),
            "restaurant_lat": d.get("restaurant_lat"),
            "restaurant_lon": d.get("restaurant_lon"),
            "customer_lat": d.get("customer_lat"),
            "customer_lon": d.get("customer_lon")
        }]), 200


@delivery_bp.route('/<delivery_id>/offer/<courier_id>', methods=['POST'])
def offer_delivery_to_courier(delivery_id, courier_id):
    """Create an OFFER relationship from system to courier for this delivery."""
    with driver.session() as session:
        if not session.run("MATCH (d:Delivery {id: $delivery_id}) RETURN d", delivery_id=delivery_id).single():
            return jsonify({"error": "Delivery not found"}), 404
        if not session.run("MATCH (u:User {id: $courier_id}) RETURN u", courier_id=courier_id).single():
            return jsonify({"error": "Courier not found"}), 404

        # idempotent offer
        session.run(
            "MATCH (u:User {id: $courier_id}), (d:Delivery {id: $delivery_id}) MERGE (u)-[r:OFFERED]->(d) SET r.ts = datetime(), r.status='pending'",
            courier_id=courier_id,
            delivery_id=delivery_id
        )
    return jsonify({'message': 'Offer created'}), 201


@delivery_bp.route('/<delivery_id>/accept', methods=['POST'])
def accept_offer(delivery_id):
    """Courier accepts the in-memory offer.
    Creates the OFFERED relation in DB with status='accepted' only at this point.
    """
    data = request.get_json(force=True)
    user_id = data.get('user_id') or data.get('courier_id')
    if not user_id:
        return jsonify({'error': 'user_id required'}), 400

    # Validate the offer exists in memory for this courier
    offer = _pending_offers.get(user_id)
    if not offer or offer['delivery_id'] != delivery_id:
        return jsonify({'error': 'No pending offer found for this courier and delivery'}), 404

    with driver.session() as session:
        if not session.run("MATCH (d:Delivery {id: $delivery_id}) RETURN d", delivery_id=delivery_id).single():
            _pending_offers.pop(user_id, None)
            return jsonify({'error': 'Delivery not found'}), 404

        # Check delivery is not already accepted/in-transit by someone else
        already_active = session.run(
            "MATCH (u:User)-[r:OFFERED]->(d:Delivery {id: $delivery_id}) "
            "WHERE r.status IN ['accepted', 'in transit'] "
            "RETURN u.id AS uid LIMIT 1",
            delivery_id=delivery_id
        ).single()
        if already_active and already_active['uid'] != user_id:
            _pending_offers.pop(user_id, None)
            return jsonify({'error': 'Delivery was already accepted by another courier'}), 409

        # Create OFFERED relation in DB with status='accepted' (first time it touches DB)
        session.run(
            "MATCH (u:User {id: $user_id}), (d:Delivery {id: $delivery_id}) "
            "MERGE (u)-[r:OFFERED]->(d) "
            "SET r.status = 'accepted', r.ts = datetime()",
            user_id=user_id,
            delivery_id=delivery_id
        )

        # Remove from in-memory pending offers
        _pending_offers.pop(user_id, None)

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
            requests.post(f"{INTERNAL_API_URL}/locations/start", json=loc_payload, timeout=2)
        except Exception:
            import traceback
            traceback.print_exc()

    print(f"[Accept] Courier {user_id} accepted delivery {delivery_id}")
    return jsonify({'message': 'Delivery accepted and assigned'}), 200


@delivery_bp.route('/<delivery_id>/reject', methods=['POST'])
def reject_offer(delivery_id):
    """Courier rejects an in-memory offer. No DB write needed – just remove from memory."""
    data = request.get_json(force=True)
    courier_id = data.get('courier_id')
    if not courier_id:
        return jsonify({'error': 'courier_id required'}), 400
    offer = _pending_offers.get(courier_id)
    if offer and offer['delivery_id'] == delivery_id:
        _pending_offers.pop(courier_id, None)
        print(f"[Reject] Courier {courier_id} rejected offer for delivery {delivery_id}")
    return jsonify({'message': 'Offer rejected'}), 200


# Courier actions: pickup, deliver, cancel
@delivery_bp.route('/<delivery_id>/pickup', methods=['POST'])
def courier_pickup(delivery_id):
    data = request.get_json(force=True)
    courier_id = data.get('courier_id')
    if not courier_id:
        return jsonify({'error': 'courier_id required'}), 400
    with driver.session() as session:
        # verify assigned with status pending
        assigned = session.run(
            "MATCH (u:User {id: $courier_id})-[r:OFFERED]->(d:Delivery {id: $delivery_id}) "
            "RETURN r.status AS status", 
            courier_id=courier_id, 
            delivery_id=delivery_id
        ).single()
        
        if not assigned:
            return jsonify({'error': 'Not assigned to this courier'}), 403
            
        status = assigned['status']
        if status != 'accepted':
            return jsonify({'error': f'Cannot pickup delivery in status {status}'}), 400
            
        session.run(
            "MATCH (u:User {id: $courier_id})-[r:OFFERED]->(d:Delivery {id: $delivery_id}) "
            "SET r.status = 'in transit', d.pickup_time = datetime()", 
            courier_id=courier_id,
            delivery_id=delivery_id
        )
        # update Redis status so location-service writes it into points
        try:
            redis_client.hset(f"pos:{courier_id}", mapping={"delivery_status": "in_transit"})
        except Exception:
            import traceback
            traceback.print_exc()
    return jsonify({'message': 'Pickup recorded'}), 200


@delivery_bp.route('/<delivery_id>/deliver', methods=['POST'])
def courier_deliver(delivery_id):
    data = request.get_json(force=True)
    courier_id = data.get('courier_id')
    if not courier_id:
        return jsonify({'error': 'courier_id required'}), 400
    with driver.session() as session:
        # verify assigned with status in transit
        assigned = session.run(
            "MATCH (u:User {id: $courier_id})-[r:OFFERED]->(d:Delivery {id: $delivery_id}) "
            "RETURN r.status AS status", 
            courier_id=courier_id, 
            delivery_id=delivery_id
        ).single()
        
        if not assigned:
            return jsonify({'error': 'Not assigned to this courier'}), 403
            
        status = assigned['status']
        if status != 'in transit':
            return jsonify({'error': f'Cannot deliver in status {status}'}), 400
            
        # mark completed
        session.run(
            "MATCH (u:User {id: $courier_id})-[r:OFFERED]->(d:Delivery {id: $delivery_id}) "
            "SET r.status = 'completed', d.delivery_time = datetime()", 
            courier_id=courier_id,
            delivery_id=delivery_id
        )
        # update Redis and stop tracking
        try:
            redis_client.hset(f"pos:{courier_id}", mapping={"delivery_status": "completed"})
        except Exception:
            import traceback
            traceback.print_exc()
        try:
            requests.post(f"{INTERNAL_API_URL}/locations/stop", json={"user_id": courier_id}, timeout=2)
        except Exception:
            import traceback
            traceback.print_exc()
    return jsonify({'message': 'Delivery marked as completed'}), 200


@delivery_bp.route('/<delivery_id>/cancel', methods=['POST'])
def courier_cancel(delivery_id):
    data = request.get_json(force=True)
    courier_id = data.get('courier_id')
    with driver.session() as session:
        # allow cancelled by assigned courier
        assigned = session.run(
            "MATCH (u:User {id: $courier_id})-[r:OFFERED]->(d:Delivery {id: $delivery_id}) "
            "RETURN r.status AS status", 
            courier_id=courier_id, 
            delivery_id=delivery_id
        ).single()
        
        if not assigned:
            return jsonify({'error': 'Not assigned to this courier'}), 403
            
        # Set status to cancelled
        session.run(
            "MATCH (u:User {id: $courier_id})-[r:OFFERED]->(d:Delivery {id: $delivery_id}) "
            "SET r.status = 'cancelled'", 
            courier_id=courier_id,
            delivery_id=delivery_id
        )
        # update Redis and stop tracking
        try:
            redis_client.hset(f"pos:{courier_id}", mapping={"delivery_status": "cancelled"})
        except Exception:
            import traceback
            traceback.print_exc()
        try:
            requests.post(f"{INTERNAL_API_URL}/locations/stop", json={"user_id": courier_id}, timeout=2)
        except Exception:
            import traceback
            traceback.print_exc()
    return jsonify({'message': 'Delivery cancelled by courier'}), 200


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculates the Haversine distance in km between two coordinate points.
    """
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


VEHICLE_CAPACITY = {
    "bicycle": 3,
    "scooter": 6,
    "car": 15,
    "van": 30,
}


def calculate_courier_score(
    courier_restaurant_dist: float,
    restaurant_customer_dist: float,
    vehicle_type: str,
    product_count: int
) -> float:
    """
    Lower score = better courier for this delivery.
    Score = weighted sum of:
      - distance from courier to restaurant (most important)
      - total route length (restaurant -> customer)
      - penalty if vehicle capacity is too small for the order
    """
    capacity = VEHICLE_CAPACITY.get(vehicle_type, 5)
    capacity_penalty = max(0, product_count - capacity) * 10.0
    score = (courier_restaurant_dist * 2.0) + (restaurant_customer_dist * 1.0) + capacity_penalty
    return score




def assign_deliveries_job():
    """
    Batch Dispatch job that runs every 20s.
    
    Rules:
    - Offers are stored IN MEMORY only (_pending_offers dict), NOT in DB.
    - A DB relation (OFFERED) is created ONLY when the courier clicks 'Accept'.
    - Deliveries with CANCELLED history (and no active relation) have priority.
    - Only couriers with is_available=True and no active DB relation (accepted/in transit)
      AND no current in-memory offer are eligible.
    """
    global _pending_offers

    with driver.session() as session:
        # 1. Find eligible deliveries:
        #    - No active DB relation (accepted / in transit)
        #    - Not currently offered in memory to someone
        #    Priority: deliveries with CANCELLED history come first.
        currently_offered_delivery_ids = {v['delivery_id'] for v in _pending_offers.values()}

        eligible_res = session.run(
            "MATCH (d:Delivery) "
            "WHERE NOT EXISTS { "
            "    MATCH (u:User)-[r:OFFERED]->(d) "
            "    WHERE r.status IN ['accepted', 'in transit', 'completed'] "
            "} "
            # Cancelled priority flag
            "OPTIONAL MATCH (u2:User)-[rc:OFFERED]->(d) WHERE rc.status = 'cancelled' "
            "RETURN d, count(rc) AS cancelled_count "
            "ORDER BY cancelled_count DESC"
        )

        deliveries = []
        for record in eligible_res:
            d = record["d"]
            if d["id"] not in currently_offered_delivery_ids:
                deliveries.append({
                    "node": d,
                    "cancelled_count": record["cancelled_count"]
                })

        if not deliveries:
            return

        # 2. Find available couriers:
        #    - is_available = true
        #    - No active DB relation (accepted / in transit)
        #    - No current in-memory offer
        couriers_with_pending_offers = set(_pending_offers.keys())

        available_couriers_res = session.run(
            "MATCH (u:User) "
            "WHERE u.account_type IN ['courier', 'delivery'] "
            "  AND COALESCE(u.is_active, true) = true "
            "  AND COALESCE(u.is_available, false) = true "
            "  AND NOT EXISTS { "
            "      MATCH (u)-[r:OFFERED]->(:Delivery) "
            "      WHERE r.status IN ['accepted', 'in transit'] "
            "  } "
            "OPTIONAL MATCH (u)-[:USES_VEHICLE]->(v:Vehicle) "
            "RETURN u.id AS id, COALESCE(v.type, 'bicycle') AS vehicle_type"
        )

        couriers = []
        for record in available_couriers_res:
            courier_id = record["id"]
            if courier_id in couriers_with_pending_offers:
                # Already has a pending in-memory offer, skip
                continue

            vehicle_type = record["vehicle_type"]
            lat, lon = None, None
            try:
                redis_data = redis_client.hgetall(f"pos:{courier_id}")
                if redis_data:
                    lat = float(redis_data.get("lat")) if redis_data.get("lat") is not None else None
                    lon = float(redis_data.get("lon")) if redis_data.get("lon") is not None else None
            except Exception:
                pass

            couriers.append({
                "id": courier_id,
                "vehicle_type": vehicle_type,
                "lat": lat,
                "lon": lon
            })

        if not couriers:
            return

        # 3. Match each delivery (priority order) to the best available courier
        for delivery_entry in deliveries:
            if not couriers:
                break

            d = delivery_entry["node"]
            delivery_id = d["id"]

            prod_count_res = session.run(
                "MATCH (d:Delivery {id: $delivery_id})-[r:CONTAINS_PRODUCT]->(:Product) "
                "RETURN count(r) AS cnt",
                delivery_id=delivery_id
            ).single()
            product_count = prod_count_res["cnt"] if prod_count_res else 0

            restaurant_lat = d.get("restaurant_lat")
            restaurant_lon = d.get("restaurant_lon")
            customer_lat = d.get("customer_lat")
            customer_lon = d.get("customer_lon")

            best_courier = None
            best_score = float('inf')

            for courier in couriers:
                if restaurant_lat is not None and restaurant_lon is not None and courier["lat"] is not None and courier["lon"] is not None:
                    courier_restaurant_distance = haversine_distance(
                        courier["lat"], courier["lon"],
                        restaurant_lat, restaurant_lon
                    )
                else:
                    courier_restaurant_distance = 1.0

                if restaurant_lat is not None and restaurant_lon is not None and customer_lat is not None and customer_lon is not None:
                    restaurant_customer_distance = haversine_distance(
                        restaurant_lat, restaurant_lon,
                        customer_lat, customer_lon
                    )
                else:
                    restaurant_customer_distance = 2.0

                score = calculate_courier_score(
                    courier_restaurant_distance,
                    restaurant_customer_distance,
                    courier["vehicle_type"],
                    product_count
                )

                if score < best_score:
                    best_score = score
                    best_courier = courier

            if best_courier:
                # Store offer in memory ONLY – no DB write yet
                _pending_offers[best_courier["id"]] = {
                    "delivery_id": delivery_id,
                    "score": best_score,
                    "offered_at": time.time()
                }
                print(f"[Scheduler] In-memory offer: delivery {delivery_id} -> courier {best_courier['id']} (score={best_score:.2f}, cancelled_history={delivery_entry['cancelled_count']})")
                couriers.remove(best_courier)


def run_scheduler():
    # Allow some startup time for DB connections to stabilize
    time.sleep(5)
    while True:
        try:
            assign_deliveries_job()
        except Exception as e:
            import traceback
            print(f"Error in delivery scheduler: {e}")
            traceback.print_exc()
        time.sleep(15)  # Batch dispatch cycle: 15 seconds


# Start the background scheduler thread
scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()




