from flask import Blueprint, request, jsonify
from db import influx_client as client, influx_bucket, influx_org

analytics_bp = Blueprint('analytics', __name__)


@analytics_bp.route('/health', methods=['GET'])
def health():
    return jsonify(status='ok')


@analytics_bp.route('/accepted-per-vehicle', methods=['GET'])
def prihvacene_po_vozilu():
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

    query = f'''
        from(bucket: "{influx_bucket}")
        |> range(start: -60d)
        |> filter(fn: (r) => r["_measurement"] == "geo_position")
        |> filter(fn: (r) => r["_field"] == "lat" or r["_field"] == "delivery_status")
        |> filter(fn: (r) => exists r.delivery_id and r.delivery_id != "")
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

    query = f'''
        from(bucket: "{influx_bucket}")
        |> range(start: -60d)
        |> filter(fn: (r) => r["_measurement"] == "geo_position")
        |> filter(fn: (r) => r["_field"] == "delivery_status")
        |> filter(fn: (r) => r["_value"] == "cancelled" or r["_value"] == "accepted")
        |> group(columns: ["user_id", "delivery_id", "_value"])
        |> first()
        |> group(columns: ["user_id"])
        |> map(fn: (r) => ({{
            r with
            is_cancelled: if r["_value"] == "cancelled" then 1.0 else 0.0,
            is_accepted: if r["_value"] == "accepted" then 1.0 else 0.0
        }}))
        |> reduce(
            identity: {{cancelled_total: 0.0, accepted_total: 0.0}},
            fn: (r, accumulator) => ({{
                cancelled_total: accumulator.cancelled_total + r.is_cancelled,
                accepted_total: accumulator.accepted_total + r.is_accepted
            }})
        )
        |> map(fn: (r) => ({{
            r with
            ratio: if r.accepted_total > 0.0 then r.cancelled_total / r.accepted_total else 0.0
        }}))
    '''
    try:
        tables = client.query_api().query(query, org=influx_org)
        res = []
        for table in tables:
            for record in table.records:
                res.append({
                    "user_id": record.values.get("user_id"),
                    "cancelled_total": record.values.get("cancelled_total"),
                    "accepted_total": record.values.get("accepted_total"),
                    "ratio": record.values.get("ratio")
                })
        return jsonify(res), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@analytics_bp.route('/hourly-accepted', methods=['GET'])
def dostave_po_satima():

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


@analytics_bp.route('/report.pdf', methods=['GET'])
def generisi_izvestaj_pdf():
    import io
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    from flask import send_file

    try:
        # 1. Prihvati podatke
        veh_data = prihvacene_po_vozilu()[0].get_json()
        range_data = opseg_kretanja()[0].get_json()
        eff_data = efikasnost_dostave()[0].get_json()
        worker_data = pouzdanost_radnika()[0].get_json()
        hourly_data = dostave_po_satima()[0].get_json()

        pdf_buf = io.BytesIO()
        with PdfPages(pdf_buf) as pdf:
            
            if veh_data:
                fig, ax = plt.subplots(figsize=(8, 6))
                vehicles = [str(x.get("vehicle_id") or "Unknown") for x in veh_data]
                counts = [x.get("accepted_count", 0) for x in veh_data]
                ax.bar(vehicles, counts, color='skyblue', edgecolor='black')
                ax.set_title("Broj prihvacenih dostava po vozilu")
                ax.set_xlabel("ID Vozila")
                ax.set_ylabel("Broj dostava")
                plt.xticks(rotation=45)
                plt.tight_layout()
                pdf.savefig(fig)
                plt.close(fig)

            
            if range_data:
                fig, ax = plt.subplots(figsize=(8, 6))
                users = [str(x.get("user_id") or "Unknown") for x in range_data]
                lat_spreads = [x.get("lat_spread") or 0.0 for x in range_data]
                lon_spreads = [x.get("lon_spread") or 0.0 for x in range_data]
                
                x_indices = range(len(users))
                width = 0.35
                ax.bar([i - width/2 for i in x_indices], lat_spreads, width, label='Lat Spread', color='lightcoral')
                ax.bar([i + width/2 for i in x_indices], lon_spreads, width, label='Lon Spread', color='aquamarine')
                ax.set_title("Opseg kretanja (Lat/Lon Spread) po korisniku")
                ax.set_xlabel("Korisnik")
                ax.set_ylabel("Opseg (Spread)")
                ax.set_xticks(x_indices)
                ax.set_xticklabels(users, rotation=45)
                ax.legend()
                plt.tight_layout()
                pdf.savefig(fig)
                plt.close(fig)

            
            if eff_data:
                fig, ax = plt.subplots(figsize=(8, 6))
                status_eff = {}
                for x in eff_data:
                    status = x.get("delivery_status") or "unknown"
                    val = x.get("mean_efficiency") or 0.0
                    status_eff[status] = status_eff.get(status, []) + [val]
                
                statuses = list(status_eff.keys())
                avg_efficiencies = [sum(v)/len(v) for v in status_eff.values()]
                ax.bar(statuses, avg_efficiencies, color='gold', edgecolor='black')
                ax.set_title("Prosecna efikasnost po statusu dostave")
                ax.set_xlabel("Status dostave")
                ax.set_ylabel("Prosecna efikasnost (duration/lat)")
                plt.tight_layout()
                pdf.savefig(fig)
                plt.close(fig)


            if worker_data:
                fig, ax = plt.subplots(figsize=(8, 6))
                users = [str(x.get("user_id") or "Unknown") for x in worker_data]
                ratios = [x.get("ratio") or 0.0 for x in worker_data]
                ax.bar(users, ratios, color='orchid', edgecolor='black')
                ax.set_title("Odnos otkazanih i prihvacenih dostava po radniku")
                ax.set_xlabel("ID Radnika")
                ax.set_ylabel("Odnos (Cancelled / Accepted)")
                plt.xticks(rotation=45)
                plt.tight_layout()
                pdf.savefig(fig)
                plt.close(fig)


            if hourly_data:
                fig, ax = plt.subplots(figsize=(8, 6))
                hours = [x.get("hour_of_day") for x in hourly_data]
                avgs = [x.get("avg_accepted_per_day", 0) for x in hourly_data]
                ax.plot(hours, avgs, marker='o', color='green', linestyle='-', linewidth=2)
                ax.set_title("Prosecan broj prihvacenih dostava po satima")
                ax.set_xlabel("Sat u danu (0-23)")
                ax.set_ylabel("Prosecan broj dostava")
                ax.set_xticks(range(0, 24, 2))
                ax.grid(True, linestyle='--', alpha=0.6)
                plt.tight_layout()
                pdf.savefig(fig)
                plt.close(fig)

        pdf_buf.seek(0)
        return send_file(
            pdf_buf,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='analiticki_izvestaj.pdf'
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
