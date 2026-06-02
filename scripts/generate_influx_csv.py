"""Generate an `influx.csv` file with realistic time-series data for demo/testing.
Columns: _time,user_id,delivery_id,lat,lon,delivery_status
Generates positions ONLY when a delivery is active.
"""
import csv
import os
from datetime import datetime, timedelta
from random import uniform, randint, choice

# Izlazni fajl u folderu iznad (workspace-root/influx.csv)
OUT = os.path.join(os.path.dirname(__file__), '..', 'influx.csv')

# Podešavanja simulacije
DRIVERS = ['user-del-1', 'user-del-2', 'user-del-3']
START_TIME = datetime(2026, 6, 1, 8, 0, 0)
BASE_LAT = 44.817
BASE_LON = 20.457

# Životni ciklus isključivo AKTIVNE dostave (bez pending-a)
STATUS_FLOW = [
    {"status": "accepted", "min_min": 3, "max_min": 6},     # Vreme do restorana
    {"status": "in_transit", "min_min": 10, "max_min": 20}, # Vreme od restorana do kupca
    {"status": "completed", "min_min": 1, "max_min": 2}     # Predaja na adresi
]

with open(OUT, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['_time', 'user_id', 'delivery_id', 'lat', 'lon', 'delivery_status'])
    
    total_rows = 0
    delivery_counter = 100
    
    for driver in DRIVERS:
        current_time = START_TIME
        
        # Početna pozicija radnika za prvu dostavu
        current_lat = BASE_LAT + uniform(-0.01, 0.01)
        current_lon = BASE_LON + uniform(-0.01, 0.01)
        
        # Svaki radnik odradi 6 dostava (jedna za drugom, sa razmakom)
        for _ in range(6): 
            delivery_id = f"del-{delivery_counter}"
            delivery_counter += 1
            
            # 5% šanse za otkazivanje (dešava se samo u fazama accepted ili in_transit)
            will_be_canceled = (randint(1, 100) <= 5)
            cancel_phase = choice(["accepted", "in_transit"]) if will_be_canceled else None
            
            delivery_interrupted = False
            
            for phase in STATUS_FLOW:
                if delivery_interrupted:
                    break
                    
                status = phase["status"]
                duration_minutes = randint(phase["min_min"], phase["max_min"])
                
                # Slučaj kada se dostava otkaže u toku ove faze
                if will_be_canceled and status == cancel_phase:
                    duration_minutes = randint(1, max(1, duration_minutes // 2))
                    end_phase_time = current_time + timedelta(minutes=duration_minutes)
                    
                    # Pišemo tačke do momenta otkazivanja
                    while current_time < end_phase_time:
                        time_str = current_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                        current_lat += uniform(-0.0012, 0.0012)
                        current_lon += uniform(-0.0012, 0.0012)
                        
                        writer.writerow([time_str, driver, delivery_id, round(current_lat, 6), round(current_lon, 6), status])
                        total_rows += 1
                        current_time += timedelta(seconds=10)
                    
                    # Upisujemo samo JEDNU finalnu tačku sa statusom 'canceled'
                    time_str = current_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                    writer.writerow([time_str, driver, delivery_id, round(current_lat, 6), round(current_lon, 6), "canceled"])
                    total_rows += 1
                    
                    delivery_interrupted = True
                    continue
                
                # Standardne aktivne faze (accepted, in_transit, completed)
                end_phase_time = current_time + timedelta(minutes=duration_minutes)
                while current_time < end_phase_time:
                    time_str = current_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                    
                    # Ako vozi, pravi veće korake, ako predaje (completed) stoji u mestu
                    step = 0.0012 if status in ["accepted", "in_transit"] else 0.0001
                    current_lat += uniform(-step, step)
                    current_lon += uniform(-step, step)
                    
                    writer.writerow([time_str, driver, delivery_id, round(current_lat, 6), round(current_lon, 6), status])
                    total_rows += 1
                    current_time += timedelta(seconds=10)
            
            # --- KLJUČNA IZMENA: RAZMAK IZMEĐU DOSTAVA ---
            # Ovde se NE UPISUJU nikakve tačke u CSV. 
            # Samo pomeramo sat unapred za 10 do 20 minuta, simulirajući pauzu do sledeće dostave.
            current_time += timedelta(minutes=randint(10, 20))
            
            # Radnik se u međuvremenu malo pomerio gradom do restorana sledeće dostave
            current_lat += uniform(-0.005, 0.005)
            current_lon += uniform(-0.005, 0.005)

print(f"Uspješno generisano {total_rows} čistih aktivnih redova u {OUT}")