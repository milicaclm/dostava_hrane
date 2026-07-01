"""
Generate an influx.csv file with realistic time-series delivery tracking data.

Columns:
_measurement,time,user_id,delivery_id,vehicle_id,lat,lon,delivery_status

Compatible with InfluxDB 2.x annotated CSV import.
"""

import csv
import os
from datetime import datetime, timedelta
from random import uniform, randint, choice

OUT = os.path.join(os.path.dirname(__file__), "..", "influx.csv")

# Simulacija
DRIVERS = ["user-del-1", "user-del-2", "user-del-3"]
VEHICLES = {
    "user-del-1": "bicycle",
    "user-del-2": "scooter",
    "user-del-3": "car"
}

START_TIME = datetime(2026, 6, 1, 8, 0, 0)

# Centrirano na Novi Sad gde aplikacija i mapa zapravo rade
BASE_LAT = 45.25
BASE_LON = 19.83

MEASUREMENT = "geo_position"

STATUS_FLOW = [
    {
        "status": "accepted",
        "min_min": 3,
        "max_min": 6,
    },
    {
        "status": "in_transit",
        "min_min": 10,
        "max_min": 20,
    },
    {
        "status": "completed",
        "min_min": 1,
        "max_min": 2,
    },
]

with open(OUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    # --------------------------------------------------
    # InfluxDB Annotated CSV header
    # --------------------------------------------------

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

    for driver in DRIVERS:
        current_time = START_TIME
        vehicle_id = VEHICLES.get(driver, "scooter")

        current_lat = BASE_LAT + uniform(-0.01, 0.01)
        current_lon = BASE_LON + uniform(-0.01, 0.01)

        # Svaki vozač odradi 6 dostava
        for _ in range(6):
            delivery_id = f"del-{delivery_counter}"
            delivery_counter += 1

            will_be_canceled = randint(1, 100) <= 5
            cancel_phase = (
                choice(["accepted", "in_transit"])
                if will_be_canceled
                else None
            )

            delivery_interrupted = False

            for phase in STATUS_FLOW:
                if delivery_interrupted:
                    break

                status = phase["status"]

                duration_minutes = randint(
                    phase["min_min"],
                    phase["max_min"],
                )

                # ------------------------------------------
                # Canceled delivery
                # ------------------------------------------
                if will_be_canceled and status == cancel_phase:
                    duration_minutes = randint(
                        1,
                        max(1, duration_minutes // 2),
                    )

                    end_phase_time = (
                        current_time +
                        timedelta(minutes=duration_minutes)
                    )

                    while current_time < end_phase_time:
                        current_lat += uniform(-0.0012, 0.0012)
                        current_lon += uniform(-0.0012, 0.0012)

                        writer.writerow([
                            MEASUREMENT,
                            current_time.strftime(
                                "%Y-%m-%dT%H:%M:%SZ"
                            ),
                            driver,
                            delivery_id,
                            vehicle_id,
                            round(current_lat, 6),
                            round(current_lon, 6),
                            status,
                        ])

                        total_rows += 1
                        current_time += timedelta(seconds=10)

                    writer.writerow([
                        MEASUREMENT,
                        current_time.strftime(
                            "%Y-%m-%dT%H:%M:%SZ"
                        ),
                        driver,
                        delivery_id,
                        vehicle_id,
                        round(current_lat, 6),
                        round(current_lon, 6),
                        "canceled",
                    ])

                    total_rows += 1
                    delivery_interrupted = True
                    continue

                # ------------------------------------------
                # Standard phases
                # ------------------------------------------
                end_phase_time = (
                    current_time +
                    timedelta(minutes=duration_minutes)
                )

                while current_time < end_phase_time:
                    step = (
                        0.0012
                        if status in ["accepted", "in_transit"]
                        else 0.0001
                    )

                    current_lat += uniform(-step, step)
                    current_lon += uniform(-step, step)

                    writer.writerow([
                        MEASUREMENT,
                        current_time.strftime(
                            "%Y-%m-%dT%H:%M:%SZ"
                        ),
                        driver,
                        delivery_id,
                        vehicle_id,
                        round(current_lat, 6),
                        round(current_lon, 6),
                        status,
                    ])

                    total_rows += 1
                    current_time += timedelta(seconds=10)

            # Pauza između dostava
            current_time += timedelta(
                minutes=randint(10, 20)
            )

            current_lat += uniform(-0.005, 0.005)
            current_lon += uniform(-0.005, 0.005)

print(
    f"Uspešno generisano {total_rows} redova u {OUT}"
)