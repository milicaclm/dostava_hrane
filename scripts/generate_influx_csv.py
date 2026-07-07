"""
Generate an influx.csv file with realistic time-series delivery tracking data.
Uses OSRM routing API to simulate natural driving paths along streets of Novi Sad.

Columns:
_measurement,time,user_id,delivery_id,vehicle_id,lat,lon,delivery_status

Compatible with InfluxDB 2.x annotated CSV import.
"""

import csv
import os
from datetime import datetime, timedelta
from random import randint, choice
import requests

OUT = os.path.join(os.path.dirname(__file__), "..", "influx.csv")

DRIVERS = ["user-del-1", "user-del-2", "user-del-3"]
VEHICLES = {
    "user-del-1": "car-1",
    "user-del-2": "scooter-1",
    "user-del-3": "bicycle-1"
}

DRIVER_START = {
    "user-del-1": (45.2423, 19.8415),
    "user-del-2": (45.2512, 19.8204),
    "user-del-3": (45.2341, 19.8282)
}

RESTAURANTS = [
    (45.2541, 19.8423),
    (45.2435, 19.8398),
    (45.2512, 19.8490)
]

CUSTOMERS = [
    (45.2392, 19.8354),
    (45.2498, 19.8032),
    (45.2612, 19.8184),
    (45.2381, 19.7990)
]

START_TIME = datetime(2026, 6, 1, 8, 0, 0)
MEASUREMENT = "geo_position"

def get_osrm_route(start_lat, start_lon, end_lat, end_lon):
    url = f"http://router.project-osrm.org/route/v1/driving/{start_lon},{start_lat};{end_lon},{end_lat}?overview=full&geometries=geojson"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            if "routes" in data and len(data["routes"]) > 0:
                coords = data["routes"][0]["geometry"]["coordinates"]
                return [(lat, lon) for lon, lat in coords]
    except Exception as e:
        print(f"OSRM API request error (falling back to linear): {e}")
    return [(start_lat, start_lon), (end_lat, end_lon)]

def sample_route(coords, num_steps):
    if not coords:
        return []
    if len(coords) == 1:
        return coords * num_steps
    
    sampled = []
    for i in range(num_steps):
        idx = (i / (num_steps - 1)) * (len(coords) - 1) if num_steps > 1 else 0
        idx_low = int(idx)
        idx_high = min(idx_low + 1, len(coords) - 1)
        weight = idx - idx_low
        
        lat = coords[idx_low][0] * (1 - weight) + coords[idx_high][0] * weight
        lon = coords[idx_low][1] * (1 - weight) + coords[idx_high][1] * weight
        sampled.append((lat, lon))
    return sampled

with open(OUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow([
        "#datatype",
        "measurement",
        "dateTime:RFC3339",
        "tag",
        "tag",
        "tag",
        "double",
        "double",
        "string",
    ])

    writer.writerow([
        "#group",
        "false",
        "false",
        "true",
        "true",
        "true",
        "false",
        "false",
        "false",
    ])

    writer.writerow([
        "#default",
        MEASUREMENT,
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    ])

    writer.writerow([
        "",
        "_measurement",
        "time",
        "user_id",
        "delivery_id",
        "vehicle_id",
        "lat",
        "lon",
        "delivery_status",
    ])

    total_rows = 0
    delivery_counter = 100

    print("Generating simulation routes...")
    for driver in DRIVERS:
        current_time = START_TIME
        vehicle_id = VEHICLES[driver]
        
        curr_lat, curr_lon = DRIVER_START[driver]

        for delivery_num in range(6):
            delivery_id = f"del-{delivery_counter}"
            delivery_counter += 1

            r_lat, r_lon = choice(RESTAURANTS)
            c_lat, c_lon = choice(CUSTOMERS)

            route_to_restaurant = get_osrm_route(curr_lat, curr_lon, r_lat, r_lon)
            route_to_customer = get_osrm_route(r_lat, r_lon, c_lat, c_lon)

            duration_acc = randint(3, 6)
            steps_acc = duration_acc * 6
            points_acc = sample_route(route_to_restaurant, steps_acc)
            
            for lat, lon in points_acc:
                writer.writerow([
                    "",
                    MEASUREMENT,
                    current_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    driver,
                    delivery_id,
                    vehicle_id,
                    round(lat, 6),
                    round(lon, 6),
                    "accepted",
                ])
                total_rows += 1
                current_time += timedelta(seconds=10)

            duration_transit = randint(10, 20)
            steps_transit = duration_transit * 6
            points_transit = sample_route(route_to_customer, steps_transit)

            for lat, lon in points_transit:
                writer.writerow([
                    "",
                    MEASUREMENT,
                    current_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    driver,
                    delivery_id,
                    vehicle_id,
                    round(lat, 6),
                    round(lon, 6),
                    "in transit",
                ])
                total_rows += 1
                current_time += timedelta(seconds=10)

            curr_lat, curr_lon = c_lat, c_lon
            writer.writerow([
                "",
                MEASUREMENT,
                current_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                driver,
                delivery_id,
                vehicle_id,
                round(curr_lat, 6),
                round(curr_lon, 6),
                "completed",
            ])
            total_rows += 1

            current_time += timedelta(minutes=randint(10, 20))

print(f"Successfully generated {total_rows} rows in {OUT}")