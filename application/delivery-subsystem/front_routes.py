from datetime import datetime
from functools import wraps
from flask import Blueprint, current_app, g, redirect, render_template, request
from flask_jwt_extended import decode_token

manager_front_bp = Blueprint("manager_front", __name__, template_folder="delivery-manager-front/templates")
courier_front_bp = Blueprint("courier_front", __name__, template_folder="courier-front/templates")

BOOL_FIELDS = {"is_active", "motorcycle_license", "car_license", "is_ready"}
FLOAT_FIELDS = {
    "salary", "average_rating", "rating", "restaurant_lat", "restaurant_lon",
    "customer_lat", "customer_lon", "weight_distance_to_restaurant",
    "weight_distance_route", "capacity_bicycle", "capacity_scooter", "capacity_car",
}


def require_role(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            token = request.cookies.get("jwt_token")
            try:
                decoded = decode_token(token) if token else {}
                if decoded.get("sub") and decoded.get("account_type") == role:
                    g.token, g.user_id = token, decoded["sub"]
                    return fn(*args, **kwargs)
            except Exception:
                pass
            return redirect("/")
        return wrapper
    return decorator


def _api(method, path, json_data=None):
    resp = current_app.test_client().open(
        path, method=method, headers={"Authorization": f"Bearer {g.token}"}, json=json_data
    )
    return resp.status_code, resp.get_json(silent=True)


def _form_payload(extra=None):
    data = {k: v.strip() for k, v in request.form.items() if k != "action" and v.strip() != ""}
    for k in BOOL_FIELDS:
        data[k] = request.form.get(k) == "on"
    for k in FLOAT_FIELDS & set(data):
        data[k] = float(data[k])
    return {**data, **(extra or {})}


def _filter(items, fields):
    q = request.args.get("q", "").strip().lower()
    if not q:
        return items
    return [x for x in items if any(q in str(x.get(f, "")).lower() for f in fields)]


def _crud_post(actions, redirect_to):
    action = request.form.get("action")
    if action not in actions:
        return None
    method, path_tpl, extra = actions[action]
    path = path_tpl.format(id=request.form.get("id", "").strip(), uid=g.user_id)
    code, data = _api(method, path, _form_payload(extra) if method in ("POST", "PUT") else None)
    if code in (200, 201):
        return redirect(redirect_to)
    return (data or {}).get("error", "Greška pri obradi zahteva.")


def _mgr():
    code, user = _api("GET", f"/users/{g.user_id}")
    return user if code == 200 and isinstance(user, dict) else {"id": g.user_id, "name": "Menadžer", "surname": "", "email": ""}


@manager_front_bp.route("/")
@require_role("manager")
def manager_index():
    return redirect("/manager/couriers")


@manager_front_bp.route("/couriers", methods=["GET", "POST"])
@require_role("manager")
def manager_couriers():
    res = _crud_post({
        "create": ("POST", "/resources/couriers", None),
        "update": ("PUT", "/resources/couriers/{id}/update", None),
        "delete": ("DELETE", "/resources/couriers/{id}", None),
    }, "/manager/couriers") if request.method == "POST" else None
    if res and not isinstance(res, str):
        return res
    _, items = _api("GET", "/resources/couriers")
    items = items.get("couriers", []) if isinstance(items, dict) else (items if isinstance(items, list) else [])
    items = _filter(items, ("id", "name", "surname", "email"))
    edit_item = next((c for c in items if c.get("id") == request.args.get("edit_id")), None)
    return render_template("couriers.html", manager=_mgr(), couriers=items, q=request.args.get("q", ""), edit_courier=edit_item, error=res, active_page="couriers")


@manager_front_bp.route("/deliveries", methods=["GET", "POST"])
@require_role("manager")
def manager_deliveries():
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    res = _crud_post({
        "create": ("POST", "/deliveries/", {"order_time": now, "start_time": now}),
        "update": ("PUT", "/deliveries/{id}", {"order_time": now, "start_time": now}),
        "delete": ("DELETE", "/deliveries/{id}", None),
    }, "/manager/deliveries") if request.method == "POST" else None
    if res and not isinstance(res, str):
        return res
    _, items = _api("GET", "/deliveries")
    items = _filter(items if isinstance(items, list) else [], ("id", "from_location", "to_location"))
    sf = request.args.get("status", "").strip().lower()
    items = [d for d in items if not sf or str(d.get("status", "")).lower() == sf]
    edit_item = next((d for d in items if d.get("id") == request.args.get("edit_id")), None)
    return render_template("deliveries.html", manager=_mgr(), deliveries=items, q=request.args.get("q", ""), status_filter=request.args.get("status", ""), edit_delivery=edit_item, error=res, active_page="deliveries")


@manager_front_bp.route("/vehicles", methods=["GET", "POST"])
@require_role("manager")
def manager_vehicles():
    res = _crud_post({
        "create": ("POST", "/resources/vehicles", {"owner_id": None}),
        "update": ("PUT", "/resources/vehicles/{id}/update", None),
        "delete": ("DELETE", "/resources/vehicles/{id}", None),
    }, "/manager/vehicles") if request.method == "POST" else None
    if res and not isinstance(res, str):
        return res
    _, items = _api("GET", "/resources/vehicles")
    items = items.get("vehicles", []) if isinstance(items, dict) else (items if isinstance(items, list) else [])
    items = _filter(items, ("id", "license_plate", "brand", "model"))
    tf = request.args.get("type", "").strip().lower()
    items = [v for v in items if not tf or str(v.get("type", "")).lower() == tf]
    edit_item = next((v for v in items if v.get("id") == request.args.get("edit_id")), None)
    return render_template("vehicles.html", manager=_mgr(), vehicles=items, q=request.args.get("q", ""), type_filter=request.args.get("type", ""), edit_vehicle=edit_item, error=res, active_page="vehicles")


@manager_front_bp.route("/parameters", methods=["GET", "POST"])
@require_role("manager")
def manager_parameters():
    msg, err = None, None
    if request.method == "POST":
        code, data = _api("PUT", "/scheduler/parameters", _form_payload())
        msg = "Parametri su uspešno sačuvani." if code == 200 else None
        err = None if code == 200 else (data or {}).get("error", "Greška pri čuvanju.")
    _, params = _api("GET", "/scheduler/parameters")
    return render_template("parameters.html", manager=_mgr(), params=params if isinstance(params, dict) else {}, message=msg, error=err, active_page="parameters")


@courier_front_bp.route("/")
@require_role("courier")
def courier_index():
    return redirect("/courier/shift")


@courier_front_bp.route("/shift", methods=["GET", "POST"])
@require_role("courier")
def courier_shift():
    err, msg = None, None
    if request.method == "POST":
        act, did = request.form.get("action"), request.form.get("delivery_id")
        if act == "accept_offer":
            code, data = _api("POST", f"/deliveries/{did}/accept", {"courier_id": g.user_id})
            if code == 200:
                return redirect(f"/courier/delivery?id={did}")
            err = (data or {}).get("error", "Nije moguće prihvatiti dostavu.")
        elif act == "set_location":
            code, data = _api("POST", f"/locations/set_position?user_id={g.user_id}", {"lat": float(request.form["lat"]), "lon": float(request.form["lon"])})
            msg = "Lokacija je sačuvana." if code in (200, 201) else None
            err = None if msg else (data or {}).get("error", "Greška pri čuvanju lokacije.")
        else:
            res = _crud_post({
                "start_shift": ("POST", "/users/{uid}/start_shift", None),
                "end_shift": ("POST", "/users/{uid}/end_shift", None),
                "reject_offer": ("POST", f"/deliveries/{did}/reject", {"courier_id": g.user_id}),
            }, "/courier/shift")
            if res and not isinstance(res, str):
                return res
            err = res
    _, user = _api("GET", f"/users/{g.user_id}")
    user = user if isinstance(user, dict) else {}
    _, pos = _api("GET", f"/locations/current_position?user_id={g.user_id}")
    _, act_del = _api("GET", f"/deliveries/active?courier_id={g.user_id}")
    _, offers = _api("GET", f"/deliveries/offers?courier_id={g.user_id}")
    return render_template("shift.html", user=user, is_active=bool(user.get("is_available", False)), position=pos if isinstance(pos, dict) else {"lat": 45.25, "lon": 19.83}, active_delivery=act_del if isinstance(act_del, dict) and act_del.get("id") else None, offers=offers if isinstance(offers, list) else [], message=msg, error=err, active_page="shift")


@courier_front_bp.route("/my-vehicles", methods=["GET", "POST"])
@require_role("courier")
def courier_vehicles():
    res = _crud_post({
        "create": ("POST", "/resources/vehicles", {"owner_id": "me", "is_ready": True}),
        "update": ("PUT", "/resources/vehicles/{id}/update", {"is_ready": True}),
        "delete": ("DELETE", "/resources/vehicles/{id}", None),
        "select": ("POST", "/users/{uid}/assign_vehicle/{id}", None),
        "unselect": ("POST", "/users/{uid}/unassign_vehicle/{id}", None),
    }, "/courier/my-vehicles") if request.method == "POST" else None
    if res and not isinstance(res, str):
        return res
    _, items = _api("GET", f"/resources/vehicles?owner_id={g.user_id}")
    items = items.get("vehicles", []) if isinstance(items, dict) else (items if isinstance(items, list) else [])
    items = _filter(items, ("id", "license_plate", "brand", "model"))
    edit_item = next((v for v in items if v.get("id") == request.args.get("edit_id")), None)
    return render_template("my_vehicles.html", current_user_id=g.user_id, vehicles=items, q=request.args.get("q", ""), edit_vehicle=edit_item, error=res, active_page="my_vehicles")


@courier_front_bp.route("/delivery", methods=["GET", "POST"])
@require_role("courier")
def courier_delivery():
    did = request.args.get("id") or request.form.get("delivery_id")
    if not did:
        return redirect("/courier/shift")
    err, msg = None, None
    if request.method == "POST":
        if request.form.get("action") == "set_location":
            code, data = _api("POST", f"/locations/set_position?user_id={g.user_id}", {"lat": float(request.form["lat"]), "lon": float(request.form["lon"])})
            msg = "Lokacija je ažurirana." if code in (200, 201) else None
            err = None if msg else (data or {}).get("error", "Greška pri ažuriranju.")
        else:
            res = _crud_post({
                "pickup": ("POST", f"/deliveries/{did}/pickup", {"courier_id": g.user_id}),
                "deliver": ("POST", f"/deliveries/{did}/deliver", {"courier_id": g.user_id}),
                "cancel": ("POST", f"/deliveries/{did}/cancel", {"courier_id": g.user_id}),
            }, "/courier/shift" if request.form.get("action") in ("deliver", "cancel") else f"/courier/delivery?id={did}")
            if res and not isinstance(res, str):
                return res
            err = res
    code, delivery = _api("GET", f"/deliveries/{did}")
    if code != 200 or not isinstance(delivery, dict):
        return redirect("/courier/shift")
    _, pos = _api("GET", f"/locations/current_position?user_id={g.user_id}")
    return render_template("delivery.html", delivery=delivery, position=pos if isinstance(pos, dict) else {"lat": 45.25, "lon": 19.83}, message=msg, error=err, active_page="shift")
