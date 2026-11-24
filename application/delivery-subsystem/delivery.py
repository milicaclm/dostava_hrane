import os
import requests
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import driver, redis_client, redis_cache, invalidate_cache
from scheduler import _pending_offers

delivery_bp = Blueprint('delivery', __name__)

INTERNAL_API_URL = os.environ.get("INTERNAL_API_URL", "http://localhost:8080")
ACTIVE_STATUSES = "['offered', 'pending', 'accepted', 'in transit', 'completed']"


def delivery_json(d, status, **extra):
    result = {"id": d["id"], "status": status, "from_location": d["from_location"], "to_location": d["to_location"]}
    for f in ["order_time", "start_time", "pickup_time", "delivery_time"]:
        result[f] = str(d[f]) if d.get(f) is not None else None
    for f in ["rating", "restaurant_lat", "restaurant_lon", "customer_lat", "customer_lon"]:
        result[f] = d.get(f)
    return {**result, **extra}


def coordinates(data):
    keys = ["restaurant_lat", "restaurant_lon", "customer_lat", "customer_lon"]
    return {k: float(data[k]) if data.get(k) is not None else None for k in keys}


def set_courier_state(courier_id, status, stop_tracking=False):
    try:
        redis_client.hset(f"pos:{courier_id}", mapping={"delivery_status": status})
    except Exception as e:
        print(f"Redis error: {e}")
    if stop_tracking:
        try:
            requests.post(f"{INTERNAL_API_URL}/locations/stop", json={"user_id": courier_id}, timeout=2)
        except Exception as e:
            print(f"Locations stop error: {e}")


@delivery_bp.route('', methods=['GET'])
@jwt_required()
def get_deliveries():
    with driver.session() as session:
        result = session.run(
            "MATCH (d:Delivery) "
            f"OPTIONAL MATCH (u:User)-[r:OFFERED]->(d) WHERE r.status IN {ACTIVE_STATUSES} "
            "RETURN d, u, r.status AS status"
        )
        deliveries = []
        for record in result:
            u = record["u"]
            courier = f"{u['id']} - {u.get('name', '')} {u.get('surname', '')}".strip() if u else None
            deliveries.append(delivery_json(record["d"], record["status"] or "placed", courier=courier))
    return jsonify(deliveries)


@delivery_bp.route('/active', methods=['GET'])
@jwt_required()
def get_active_delivery():
    with driver.session() as session:
        result = session.run(
            "MATCH (u:User {id: $courier_id})-[r:OFFERED]->(d:Delivery) "
            "WHERE r.status IN ['accepted', 'in transit'] RETURN d, r.status AS status",
            courier_id=get_jwt_identity()
        ).single()
    return jsonify(delivery_json(result["d"], result["status"]) if result else None), 200


@delivery_bp.route('/<delivery_id>')
@redis_cache("delivery")
def get_delivery(delivery_id):
    with driver.session() as session:
        record = session.run(
            "MATCH (d:Delivery {id: $delivery_id}) "
            f"OPTIONAL MATCH (u:User)-[r:OFFERED]->(d) WHERE r.status IN {ACTIVE_STATUSES} "
            "RETURN d, u, r.status AS status",
            delivery_id=delivery_id
        ).single()
        if not record:
            return jsonify({"error": "Delivery not found"}), 404

        u = record["u"]
        courier = f"{u['id']} - {u.get('name', '')} {u.get('surname', '')}".strip() if u else None
        vehicle_type = "bicycle"
        if u:
            vehicle = session.run(
                "MATCH (u:User {id: $user_id})-[:USES_VEHICLE]->(v:Vehicle) RETURN v.type AS type LIMIT 1",
                user_id=u["id"]
            ).single()
            vehicle_type = vehicle["type"] if vehicle else vehicle_type

        products = session.run(
            "MATCH (d:Delivery {id: $delivery_id})-[r:CONTAINS_PRODUCT]->(:Product) RETURN sum(coalesce(r.quantity, 1)) AS cnt",
            delivery_id=delivery_id
        ).single()
        return jsonify(delivery_json(record["d"], record["status"] or "placed", courier=courier,
                                     vehicle_type=vehicle_type, product_count=products["cnt"] if products else 0))


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
            **coordinates(data)
        )
    return jsonify({"message": "Delivery created successfully"}), 201


@delivery_bp.route('/<delivery_id>', methods=['PUT'])
@invalidate_cache("delivery")
def update_delivery(delivery_id):
    data = request.get_json()
    with driver.session() as session:
        record = session.run(
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
            **coordinates(data)
        ).single()
    if not record:
        return jsonify({"error": "Delivery not found"}), 404
    return jsonify(delivery_json(record["d"], "placed"))


@delivery_bp.route('/<delivery_id>', methods=['DELETE'])
@invalidate_cache("delivery")
def delete_delivery(delivery_id):
    with driver.session() as session:
        record = session.run(
            "MATCH (d:Delivery {id: $delivery_id}) DETACH DELETE d RETURN COUNT(d) AS deleted_count",
            delivery_id=delivery_id
        ).single()
    if record["deleted_count"] > 0:
        return jsonify({"message": "Delivery deleted successfully"})
    return jsonify({"error": "Delivery not found"}), 404


@delivery_bp.route('/<delivery_id>/products', methods=['POST'])
@invalidate_cache("delivery")
def add_product_to_delivery(delivery_id):
    product_id = request.get_json()["product_id"]
    with driver.session() as session:
        record = session.run(
            "MATCH (d:Delivery {id: $delivery_id}), (p:Product {id: $product_id}) "
            "CREATE (d)-[:CONTAINS_PRODUCT]->(p) RETURN p",
            delivery_id=delivery_id, product_id=product_id
        ).single()
    if not record:
        return jsonify({"error": "Delivery or Product not found"}), 404
    p = record["p"]
    return jsonify({"product": {"id": p["id"], "name": p["name"], "description": p["description"], "price": p["price"]}})


@delivery_bp.route('/<delivery_id>/products/<product_id>', methods=['DELETE'])
@invalidate_cache("delivery")
def remove_product_from_delivery(delivery_id, product_id):
    with driver.session() as session:
        record = session.run(
            "MATCH (d:Delivery {id: $delivery_id})-[r:CONTAINS_PRODUCT]->(p:Product {id: $product_id}) "
            "DELETE r RETURN COUNT(r) AS deleted_count",
            delivery_id=delivery_id, product_id=product_id
        ).single()
    if record["deleted_count"] > 0:
        return jsonify({"message": "Product removed from delivery successfully"})
    return jsonify({"error": "Delivery or Product not found"}), 404


@delivery_bp.route('/<delivery_id>/products', methods=['GET'])
def get_delivery_products(delivery_id):
    with driver.session() as session:
        result = session.run(
            "MATCH (d:Delivery {id: $delivery_id})-[:CONTAINS_PRODUCT]->(p:Product) RETURN p",
            delivery_id=delivery_id
        )
        products = [{"id": r["p"]["id"], "name": r["p"]["name"], "description": r["p"]["description"], "price": r["p"]["price"]} for r in result]
    return jsonify({"products": products})


@delivery_bp.route('/offers', methods=['GET'])
@jwt_required()
def get_offered_deliveries():
    courier_id = get_jwt_identity()
    offer = _pending_offers.get(courier_id)
    if not offer:
        return jsonify([]), 200
    with driver.session() as session:
        result = session.run("MATCH (d:Delivery {id: $delivery_id}) RETURN d", delivery_id=offer["delivery_id"]).single()
    if not result:
        _pending_offers.pop(courier_id, None)
        return jsonify([]), 200
    return jsonify([delivery_json(result["d"], "pending")]), 200


@delivery_bp.route('/<delivery_id>/accept', methods=['POST'])
@invalidate_cache("delivery")
def accept_offer(delivery_id):
    data = request.get_json(force=True)
    user_id = data.get('user_id') or data.get('courier_id')
    if not user_id:
        return jsonify({'error': 'user_id required'}), 400

    offer = _pending_offers.get(user_id)
    if not offer or offer['delivery_id'] != delivery_id:
        return jsonify({'error': 'No pending offer found for this courier and delivery'}), 404

    with driver.session() as session:
        pending = session.run(
            "MATCH (u:User {id: $user_id})-[r:OFFERED {status: 'pending'}]->(d:Delivery {id: $delivery_id}) RETURN r LIMIT 1",
            user_id=user_id, delivery_id=delivery_id
        ).single()
        if not pending:
            _pending_offers.pop(user_id, None)
            return jsonify({'error': 'No pending offer found in the database for this courier and delivery'}), 404

        session.run(
            "MATCH (u:User {id: $user_id})-[r:OFFERED]->(d:Delivery {id: $delivery_id}) "
            "SET r.status = 'accepted', r.ts = datetime()",
            user_id=user_id, delivery_id=delivery_id
        )
        vehicle = session.run(
            "MATCH (u:User {id: $user_id})-[:USES_VEHICLE]->(v:Vehicle) RETURN v.license_plate AS lp LIMIT 1",
            user_id=user_id
        ).single()
    vehicle_id = vehicle["lp"] if vehicle else ""
    _pending_offers.pop(user_id, None)

    try:
        redis_client.hset(f"pos:{user_id}", mapping={"delivery_id": delivery_id, "delivery_status": "accepted", "vehicle_id": vehicle_id})
        payload = {"user_id": user_id, "delivery_id": delivery_id, "delivery_status": "accepted", "vehicle_id": vehicle_id}
        requests.post(f"{INTERNAL_API_URL}/locations/start", json=payload, timeout=2)
    except Exception as e:
        print(f"Accept side effects error: {e}")
    return jsonify({'message': 'Delivery accepted and assigned'}), 200


@delivery_bp.route('/<delivery_id>/reject', methods=['POST'])
@invalidate_cache("delivery")
def reject_offer(delivery_id):
    courier_id = request.get_json(force=True).get('courier_id')
    if not courier_id:
        return jsonify({'error': 'courier_id required'}), 400

    with driver.session() as session:
        session.run(
            "MATCH (u:User {id: $user_id})-[r:OFFERED {status: 'pending'}]->(d:Delivery {id: $delivery_id}) DELETE r",
            user_id=courier_id, delivery_id=delivery_id
        )
    try:
        redis_client.sadd(f"rejected:{courier_id}", delivery_id)
        redis_client.expire(f"rejected:{courier_id}", 600)
    except Exception as e:
        print(f"Error saving rejection to Redis: {e}")

    offer = _pending_offers.get(courier_id)
    if offer and offer['delivery_id'] == delivery_id:
        _pending_offers.pop(courier_id, None)
    return jsonify({'message': 'Offer rejected'}), 200


def change_status(delivery_id, allowed, new_status, extra_cypher, redis_status, stop_tracking=False):
    courier_id = request.get_json(force=True).get('courier_id')
    if not courier_id:
        return jsonify({'error': 'courier_id required'}), 400
    match = "MATCH (u:User {id: $courier_id})-[r:OFFERED]->(d:Delivery {id: $delivery_id}) "
    with driver.session() as session:
        current = session.run(match + "RETURN r.status AS status", courier_id=courier_id, delivery_id=delivery_id).single()
        if not current:
            return jsonify({'error': 'Not assigned to this courier'}), 403
        if allowed and current['status'] != allowed:
            return jsonify({'error': f"Cannot change delivery in status {current['status']}"}), 400
        session.run(match + "SET r.status = $status " + extra_cypher,
                    courier_id=courier_id, delivery_id=delivery_id, status=new_status)
    set_courier_state(courier_id, redis_status, stop_tracking)
    return jsonify({'message': f'Delivery {new_status}'}), 200


@delivery_bp.route('/<delivery_id>/pickup', methods=['POST'])
@invalidate_cache("delivery")
def courier_pickup(delivery_id):
    return change_status(delivery_id, 'accepted', 'in transit', ", d.pickup_time = datetime()", "in_transit")


@delivery_bp.route('/<delivery_id>/deliver', methods=['POST'])
@invalidate_cache("delivery")
def courier_deliver(delivery_id):
    return change_status(delivery_id, 'in transit', 'completed', ", d.delivery_time = datetime()", "completed", True)


@delivery_bp.route('/<delivery_id>/cancel', methods=['POST'])
@invalidate_cache("delivery")
def courier_cancel(delivery_id):
    return change_status(delivery_id, None, 'cancelled', "REMOVE d.pickup_time, d.delivery_time", "cancelled", True)
