from flask import Blueprint, request, jsonify
from db import influx_client as client, influx_bucket, influx_org

analytics_bp = Blueprint('analytics', __name__)


@analytics_bp.route('/health', methods=['GET'])
def health():
    return jsonify(status='ok')


@analytics_bp.route('/accepted-per-vehicle', methods=['GET'])
def prihvacene_po_vozilu():
    """
    1. Ukupan broj zapisa sa statusom 'accepted' po vehicle_id.
    Filtriranje po merenju i polju, grupisanje po vehicle_id,
    agregacija count() i sortiranje od najvećeg ka najmanjem.
    """
    query = f'''
        from(bucket: "{influx_bucket}")
        |> range(start: -60d)
        |> filter(fn: (r) => r["_measurement"] == "geo_position")
        |> filter(fn: (r) => r["_field"] == "delivery_status")
        |> filter(fn: (r) => r["_value"] == "accepted")
        |> group(columns: ["vehicle_id", "delivery_id"])
        |> first()
        |> group(columns: ["vehicle_id"])
        |> count()
        |> sort(columns: ["_value"], desc: true)
    '''
    try:
        tables = client.query_api().query(query, org=influx_org)
        res = []
        for table in tables:
            for record in table.records:
                res.append({
                    "vehicle_id": record.values.get("vehicle_id"),
                    "accepted_count": record.get_value()
                })
        return jsonify(res), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@analytics_bp.route('/movement-range', methods=['GET'])
def opseg_kretanja():
    """
    2. Opseg kretanja (spread) latitude i longitude po korisniku (user_id).
    Koristi spread() i pivot() da prikaze obe koordinate u jednoj tabeli po korisniku.
    """
    query = f'''
        from(bucket: "{influx_bucket}")
        |> range(start: -60d)
        |> filter(fn: (r) => r["_measurement"] == "geo_position")
        |> filter(fn: (r) => r["_field"] == "lat" or r["_field"] == "lon")
        |> group(columns: ["user_id", "_field"])
        |> spread()
        |> group(columns: ["user_id"])
        |> pivot(rowKey: ["user_id"], columnKey: ["_field"], valueColumn: "_value")
    '''
    try:
        tables = client.query_api().query(query, org=influx_org)
        res = []
        for table in tables:
            for record in table.records:
                res.append({
                    "user_id": record.values.get("user_id"),
                    "lat_spread": record.values.get("lat"),
                    "lon_spread": record.values.get("lon")
                })
        return jsonify(res), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@analytics_bp.route('/delivery-efficiency', methods=['GET'])
def efikasnost_dostave():
    """
    3. Efikasnost po dostavi (delivery_id) i statusu.
    Pivotira delivery_status i lat po vremenu, koristi elapsed() za trajanje,
    map() za apsolutne vrednosti, filtrira lat <= 0 i računa efficiency = duration / lat.
    Grupise po delivery_id i delivery_status i izracunava mean(efikasnosti).
    """
    query = f'''
        from(bucket: "{influx_bucket}")
        |> range(start: -60d)
        |> filter(fn: (r) => r["_measurement"] == "geo_position")
        |> filter(fn: (r) => r["_field"] == "lat" or r["_field"] == "delivery_status")
        |> pivot(rowKey: ["_time", "delivery_id"], columnKey: ["_field"], valueColumn: "_value")
        |> group(columns: ["delivery_id"])
        |> elapsed(unit: 1s, timeColumn: "_time", columnName: "duration_s")
        |> map(fn: (r) => ({{
            r with
            duration_s: if r.duration_s < 0 then -r.duration_s else r.duration_s,
            lat_float: float(v: string(v: r.lat))
        }}))
        |> filter(fn: (r) => r.lat_float > 0.0)
        |> map(fn: (r) => ({{
            r with
            efficiency: float(v: r.duration_s) / r.lat_float,
            _value: float(v: r.duration_s) / r.lat_float
        }}))
        |> group(columns: ["delivery_id", "delivery_status"])
        |> mean(column: "_value")
    '''
    try:
        tables = client.query_api().query(query, org=influx_org)
        res = []
        for table in tables:
            for record in table.records:
                res.append({
                    "delivery_id": record.values.get("delivery_id"),
                    "delivery_status": record.values.get("delivery_status"),
                    "mean_efficiency": record.get_value()
                })
        return jsonify(res), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@analytics_bp.route('/worker-reliability', methods=['GET'])
def pouzdanost_radnika():
    """
    4. Analiza pouzdanosti radnika.
    Broji jedinstvene prihvaćene i otkazane dostave po radniku (user_id).
    Zatim izračunava njihov odnos (canceled / accepted).
    """
    query = f'''
        from(bucket: "{influx_bucket}")
        |> range(start: -60d)
        |> filter(fn: (r) => r["_measurement"] == "geo_position")
        |> filter(fn: (r) => r["_field"] == "delivery_status")
        |> filter(fn: (r) => r["_value"] == "canceled" or r["_value"] == "accepted")
        |> group(columns: ["user_id", "delivery_id", "_value"])
        |> first()
        |> group(columns: ["user_id"])
        |> map(fn: (r) => ({{
            r with
            is_canceled: if r["_value"] == "canceled" then 1.0 else 0.0,
            is_accepted: if r["_value"] == "accepted" then 1.0 else 0.0
        }}))
        |> reduce(
            identity: {{canceled_total: 0.0, accepted_total: 0.0}},
            fn: (r, accumulator) => ({{
                canceled_total: accumulator.canceled_total + r.is_canceled,
                accepted_total: accumulator.accepted_total + r.is_accepted
            }})
        )
        |> map(fn: (r) => ({{
            r with
            ratio: if r.accepted_total > 0.0 then r.canceled_total / r.accepted_total else 0.0
        }}))
    '''
    try:
        tables = client.query_api().query(query, org=influx_org)
        res = []
        for table in tables:
            for record in table.records:
                res.append({
                    "user_id": record.values.get("user_id"),
                    "canceled_total": record.values.get("canceled_total"),
                    "accepted_total": record.values.get("accepted_total"),
                    "ratio": record.values.get("ratio")
                })
        return jsonify(res), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@analytics_bp.route('/hourly-accepted', methods=['GET'])
def dostave_po_satima():
    """
    5. Raspodela prihvaćenih dostava po satu u prosečnom danu.
    Za svaki sat u danu (0-23) računa prosečan broj dostava
    uzimajući u obzir sve dostupne dane u datasetu.
    """
    query = f'''
        import "date"

        from(bucket: "{influx_bucket}")
        |> range(start: -60d)
        |> filter(fn: (r) => r["_measurement"] == "geo_position")
        |> filter(fn: (r) => r["_field"] == "delivery_status")
        |> filter(fn: (r) => r["_value"] == "accepted")
        |> group(columns: ["delivery_id"])
        |> first()
        |> group(columns: [])
        |> aggregateWindow(every: 1h, fn: count, createEmpty: false)
        |> map(fn: (r) => ({{r with hour_of_day: date.hour(t: r._time)}}))
        |> group(columns: ["hour_of_day"])
        |> mean(column: "_value")
        |> sort(columns: ["hour_of_day"], desc: false)
    '''
    try:
        tables = client.query_api().query(query, org=influx_org)
        res = []
        for table in tables:
            for record in table.records:
                res.append({
                    "hour_of_day": record.values.get("hour_of_day"),
                    "avg_accepted_per_day": round(record.get_value(), 2)
                })
        return jsonify(res), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
