from flask import Blueprint, request, jsonify
from db import influx_client as client, influx_bucket, influx_org

analitics_bp = Blueprint('analitics', __name__)
write_api = client.write_api()


@analitics_bp.route('/health', methods=['GET'])
def health():
    return jsonify(status='ok')


@analitics_bp.route('/efficiency', methods=['GET'])
def analiza_efikasnosti():
    data = request.get_json(silent=True) or {}
    user_id = request.args.get('user_id') or data.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
    delivery_id = request.args.get('delivery_id') or data.get('delivery_id')
    
    delivery_filter = f'and r["delivery_id"] == "{delivery_id}"' if delivery_id else ''
    
    query = f'''
        from(bucket: "{influx_bucket}")
        |> range(start: -24h)
        |> filter(fn: (r) => r["_measurement"] == "geo_position" and r["user_id"] == "{user_id}" {delivery_filter})
        |> filter(fn: (r) => r["_field"] == "delivery_status")
        |> elapsed(unit: 1s, timeColumn: "_time", columnName: "duration")
        |> group(columns: ["_value"])
        |> sum(column: "duration")
        |> sort(columns: ["duration"], desc: true)
    '''
    try:
        tables = client.query_api().query(query, org=influx_org)
        res = []
        for table in tables:
            for record in table.records:
                res.append({
                    "status": record.values.get("_value"),
                    "duration_seconds": record.get_value()
                })
        return jsonify(res), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@analitics_bp.route('/geographical-range', methods=['GET'])
def geografski_opseg():
    # Detektuje najveći opseg kretanja dostavljača na osnovu lat i lon devijacija
    query = f'''
        from(bucket: "{influx_bucket}")
        |> range(start: -24h)
        |> filter(fn: (r) => r["_measurement"] == "geo_position")
        |> filter(fn: (r) => r["_field"] == "lat" or r["_field"] == "lon")
        |> group(columns: ["user_id", "_field"])
        |> aggregateWindow(every: 1h, fn: spread, createEmpty: false)
        |> group(columns: ["user_id"])
        |> sum()
        |> sort(columns: ["_value"], desc: true)
    '''
    try:
        tables = client.query_api().query(query, org=influx_org)
        res = {}
        for table in tables:
            for record in table.records:
                uid = record.values.get("user_id")
                val = record.get_value()
                if uid not in res:
                    res[uid] = 0.0
                res[uid] += val if val else 0.0
        
        sorted_res = sorted([{"user_id": k, "spread_score": v} for k, v in res.items()], key=lambda x: x["spread_score"], reverse=True)
        return jsonify(sorted_res), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@analitics_bp.route('/idle-time', methods=['GET'])
def mrtav_hod():
    # Detektuje dostavljače koji stoje u mestu a nemaju aktivnu dostavu (standardna devijacija koordinata blizu nule)
    query = f'''
        from(bucket: "{influx_bucket}")
        |> range(start: -6h)
        |> filter(fn: (r) => r["_measurement"] == "geo_position" and (r["delivery_id"] == "" or r["delivery_id"] == "None"))
        |> filter(fn: (r) => r["_field"] == "lat" or r["_field"] == "lon")
        |> group(columns: ["user_id", "_field"])
        |> aggregateWindow(every: 5m, fn: stddev, createEmpty: false)
        |> filter(fn: (r) => r["_value"] < 0.0001)
        |> group(columns: ["user_id"])
        |> count()
        |> sort(columns: ["_value"], desc: true)
    '''
    try:
        tables = client.query_api().query(query, org=influx_org)
        res = []
        for table in tables:
            for record in table.records:
                res.append({
                    "user_id": record.values.get("user_id"),
                    "idle_5min_intervals": record.get_value()
                })
        return jsonify(res), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@analitics_bp.route('/connection-stability', methods=['GET'])
def stabilnost_konekcije():
    # Detektuje prekide u prenosu lokacije (kašnjenje veće od 10 sekundi)
    query = f'''
        from(bucket: "{influx_bucket}")
        |> range(start: -1h)
        |> filter(fn: (r) => r["_measurement"] == "geo_position")
        |> filter(fn: (r) => r["_field"] == "lat")
        |> group(columns: ["user_id"])
        |> elapsed(unit: 1s, timeColumn: "_time", columnName: "gap_duration")
        |> filter(fn: (r) => r["gap_duration"] > 10)
        |> sort(columns: ["gap_duration"], desc: true)
    '''
    try:
        tables = client.query_api().query(query, org=influx_org)
        res = []
        for table in tables:
            for record in table.records:
                res.append({
                    "user_id": record.values.get("user_id"),
                    "gap_duration_seconds": record.values.get("gap_duration"),
                    "time": record.get_time()
                })
        return jsonify(res), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



#TODO:generisati dovoljno uzoraka i popraviti influx