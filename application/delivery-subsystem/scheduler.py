import math
import time
import threading
import numpy as np
from scipy.optimize import linear_sum_assignment
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from db import driver, redis_client

scheduler_bp = Blueprint('scheduler', __name__)

_pending_offers: dict = {}

PARAM_DEFAULTS = {
    "weight_distance_to_restaurant": 0.5,
    "weight_distance_route": 0.5,
    "capacity_bicycle": 3.0,
    "capacity_scooter": 6.0,
    "capacity_car": 15.0,
}


def get_dynamic_params():
    params = {}
    for k, default in PARAM_DEFAULTS.items():
        val = redis_client.get(f"params:{k}")
        params[k] = float(val) if val is not None else default
    return params


@scheduler_bp.route('/parameters', methods=['GET'])
@jwt_required()
def get_parameters():
    try:
        return jsonify(get_dynamic_params()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@scheduler_bp.route('/parameters', methods=['PUT'])
@jwt_required()
def update_parameters():
    data = request.json
    for k in PARAM_DEFAULTS:
        if k in data:
            redis_client.set(f"params:{k}", str(data[k]))
    return jsonify({'message': 'Parameters updated successfully'}), 200


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def calculate_courier_score(
    courier_restaurant_dist: float,
    restaurant_customer_dist: float,
    vehicle_type: str,
    product_count: int,
    params: dict
) -> float:
    v_type = vehicle_type
    if v_type in ['bike', 'motorcycle']:
        v_type = 'scooter'

    cap_key = f"capacity_{v_type}"
    capacity = params.get(cap_key, params.get("capacity_bicycle"))

    max_cap = params.get("capacity_car", 15.0)
    if product_count > max_cap:
        return 1e9

    if product_count > capacity:
        return 1e9

    speed_factors = {
        "car": 3.0,
        "scooter": 2.0,
        "bicycle": 1.0
    }
    speed_factor = speed_factors.get(v_type, 1.0)
    adjusted_dist = courier_restaurant_dist / speed_factor

    score = (adjusted_dist * params["weight_distance_to_restaurant"]) + (restaurant_customer_dist * params["weight_distance_route"])
    return score


def assign_deliveries_job():
    now_time = time.time()
    params = get_dynamic_params()

    with driver.session() as session:
        expired_couriers = [cid for cid, offer in _pending_offers.items() if now_time - offer['offered_at'] >= 15.0]
        for cid in expired_couriers:
            del_id = _pending_offers[cid]['delivery_id']
            print(f"[Scheduler] Expiring pending offer for courier {cid} (delivery {del_id}) due to timeout", flush=True)
            session.run(
                "MATCH (u:User {id: $user_id})-[r:OFFERED {status: 'pending'}]->(d:Delivery {id: $delivery_id}) "
                "DELETE r",
                user_id=cid,
                delivery_id=del_id
            )
            _pending_offers.pop(cid, None)

        currently_offered_delivery_ids = {v['delivery_id'] for v in _pending_offers.values()}

        eligible_res = session.run(
            "MATCH (d:Delivery) "
            "WHERE NOT EXISTS { "
            "    MATCH (u:User)-[r:OFFERED]->(d) "
            "    WHERE r.status IN ['accepted', 'in transit', 'completed'] "
            "} "
            "OPTIONAL MATCH (u2:User)-[rc:OFFERED]->(d) WHERE rc.status IN ['cancelled', 'rejected'] "
            "RETURN d, count(rc) AS cancelled_count "
            "ORDER BY cancelled_count DESC"
        )

        deliveries = []
        for record in eligible_res:
            d = record["d"]
            if d["id"] not in currently_offered_delivery_ids:
                deliveries.append({"node": d, "cancelled_count": record["cancelled_count"]})

        if not deliveries:
            return

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

        ignored_pairs = set()
        for courier in couriers:
            try:
                rejected_ids = redis_client.smembers(f"rejected:{courier['id']}")
                for rid in rejected_ids:
                    ignored_pairs.add((courier['id'], rid))
            except Exception as e:
                print(f"Error reading rejections from Redis: {e}")

        cancelled_res = session.run(
            "MATCH (u:User)-[r:OFFERED]->(d:Delivery) "
            "WHERE r.status = 'cancelled' "
            "RETURN u.id AS user_id, d.id AS delivery_id"
        )
        for record in cancelled_res:
            ignored_pairs.add((record["user_id"], record["delivery_id"]))

        cost_matrix = np.zeros((len(deliveries), len(couriers)))
        for i, delivery_entry in enumerate(deliveries):
            d = delivery_entry["node"]
            delivery_id = d["id"]

            prod_count_res = session.run(
                "MATCH (d:Delivery {id: $delivery_id})-[r:CONTAINS_PRODUCT]->(:Product) "
                "RETURN sum(coalesce(r.quantity, 1)) AS cnt",
                delivery_id=delivery_id
            ).single()
            product_count = prod_count_res["cnt"] if prod_count_res else 0

            restaurant_lat = d.get("restaurant_lat")
            restaurant_lon = d.get("restaurant_lon")
            customer_lat = d.get("customer_lat")
            customer_lon = d.get("customer_lon")

            for j, courier in enumerate(couriers):
                if (courier["id"], delivery_id) in ignored_pairs:
                    cost_matrix[i, j] = 1e9
                    continue

                courier_restaurant_distance = 0.0
                restaurant_customer_distance = 0.0
                
                if courier["lat"] is None or courier["lon"] is None or (courier["lat"] == 0.0 and courier["lon"] == 0.0):
                    courier_restaurant_distance = 1000.0
                elif restaurant_lat is not None and restaurant_lon is not None:
                    courier_restaurant_distance = haversine_distance(
                        courier["lat"], courier["lon"],
                        restaurant_lat, restaurant_lon
                    )

                if restaurant_lat is not None and restaurant_lon is not None and customer_lat is not None and customer_lon is not None:
                    restaurant_customer_distance = haversine_distance(
                        restaurant_lat, restaurant_lon,
                        customer_lat, customer_lon
                    )

                score = calculate_courier_score(
                    courier_restaurant_distance,
                    restaurant_customer_distance,
                    courier["vehicle_type"],
                    product_count,
                    params
                )
                cost_matrix[i, j] = score

        row_ind, col_ind = linear_sum_assignment(cost_matrix)
        for i, j in zip(row_ind, col_ind):
            best_score = cost_matrix[i, j]
            if best_score >= 1e9:
                print(f"[Scheduler] Skipping assignment of delivery {deliveries[i]['node']['id']} because matched courier has insufficient capacity (score={best_score:.2f})")
                continue

            best_courier = couriers[j]
            delivery_id = deliveries[i]["node"]["id"]

            _pending_offers[best_courier["id"]] = {
                "delivery_id": delivery_id,
                "score": best_score,
                "offered_at": time.time()
            }
            session.run(
                "MATCH (u:User {id: $user_id}), (d:Delivery {id: $delivery_id}) "
                "MERGE (u)-[r:OFFERED]->(d) "
                "SET r.status = 'pending', r.ts = datetime()",
                user_id=best_courier["id"],
                delivery_id=delivery_id
            )
            print(f"[Scheduler] In-memory offer: delivery {delivery_id} -> courier {best_courier['id']} (score={best_score:.2f})")


def run_scheduler():
    time.sleep(5)
    while True:
        try:
            assign_deliveries_job()
        except Exception as e:
            import traceback
            err_name = type(e).__name__
            err_mod = type(e).__module__
            if "ServiceUnavailable" in err_name or "ConnectionRefusedError" in err_name:
                print(f"[Scheduler] Database (Neo4j) is not ready yet.", flush=True)
            elif "ConnectionError" in err_name and "redis" in err_mod:
                print(f"[Scheduler] Redis is not ready yet.", flush=True)
            else:
                print(f"Error in delivery scheduler: {e}", flush=True)
                traceback.print_exc()
        time.sleep(15)


scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()
