from flask import Blueprint, request, jsonify
from db import influx_client as client, influx_bucket, influx_org
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from flask import send_file

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
        |> group()
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




@analytics_bp.route('/courier-active-time', methods=['GET'])
def aktivno_vreme_kurira():
    query = f'''
        from(bucket: "{influx_bucket}")
        |> range(start: -60d)
        |> filter(fn: (r) => r["_measurement"] == "geo_position")
        |> filter(fn: (r) => r["_field"] == "lat")
        |> filter(fn: (r) => r._value > 1.0)
        |> group(columns: ["user_id"])
        |> count()
        |> group()
        |> sort(columns: ["_value"], desc: true)
    '''
    try:
        tables = client.query_api().query(query, org=influx_org)
        res = []
        for table in tables:
            for record in table.records:
                res.append({
                    "user_id": record.values.get("user_id"),
                    "activity_time": record.get_value()
                })
        return jsonify(res), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@analytics_bp.route('/cancelled-by-courier', methods=['GET'])
def otkazanih_po_radniku():
    query = f'''
        from(bucket: "{influx_bucket}")
        |> range(start: -60d)
        |> filter(fn: (r) => r["_measurement"] == "geo_position")
        |> filter(fn: (r) => r["_field"] == "delivery_status")
        |> filter(fn: (r) => r["_value"] == "cancelled")
        |> group(columns: ["user_id", "delivery_id"])
        |> first()
        |> group(columns: ["user_id"])
        |> count()
        |> group()
        |> sort(columns: ["_value"], desc: true)
    '''
    try:
        tables = client.query_api().query(query, org=influx_org)
        res = []
        for table in tables:
            for record in table.records:
                res.append({
                    "user_id": record.values.get("user_id"),
                    "cancelled_count": record.get_value()
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
        |> group()
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
    
    try:
        veh_data = prihvacene_po_vozilu()[0].get_json()
        activity_data = aktivno_vreme_kurira()[0].get_json()
        cancelled_data = otkazanih_po_radniku()[0].get_json()
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


            
            if activity_data:
                fig, ax = plt.subplots(figsize=(8, 6))
                users = [str(x.get("user_id") or "Unknown") for x in activity_data]
                activity_times = [x.get("activity_time", 0) for x in activity_data]
                ax.bar(users, activity_times, color='gold', edgecolor='black')
                ax.set_title("Vreme aktivnosti po radniku (broj signala)")
                ax.set_xlabel("Korisnik")
                ax.set_ylabel("Broj signala")
                plt.xticks(rotation=45)
                plt.tight_layout()
                pdf.savefig(fig)
                plt.close(fig)


            if cancelled_data:
                fig, ax = plt.subplots(figsize=(8, 6))
                users = [str(x.get("user_id") or "Unknown") for x in cancelled_data]
                cancelled_counts = [x.get("cancelled_count") or 0 for x in cancelled_data]
                ax.bar(users, cancelled_counts, color='orchid', edgecolor='black')
                ax.set_title("Broj otkazanih dostava po radniku")
                ax.set_xlabel("ID Radnika")
                ax.set_ylabel("Broj otkazanih dostava")
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
