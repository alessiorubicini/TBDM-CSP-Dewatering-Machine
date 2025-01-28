### This script simulates constant sensor data with drift and anomalies, and writes it to InfluxDB.

import time
import random
from influxdb_client import InfluxDBClient, Point, WriteOptions

# Configuration
bucket = "dewatering_machine_live"
org = "Unicam"
token = "omwIAYPdPo6T7k1VMMwO8OevYJmQ8Tj3xMYijRP7dkGz9FMxCJQB8VWsQnl5CAYxT99tn32CJV5zTJmOGx-9xQ=="
url = "http://localhost:8086"

# Initialize InfluxDB Client
client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=WriteOptions(batch_size=1))

# Define baselines and ranges
BASELINES = {
    "portata_fanghi": 30,  # m³/h
    "portata_poly": 0.3,   # L/h
    "torbidita_chiarificato": 2.5,  # NTU
    "torbidita_fango": 100,  # NTU
    "umidita_fango": 70,  # %
    "velocita_coclea": 70,  # RPM
    "velocita_tamburo": 2750,  # RPM
}
RANGES = {
    "portata_fanghi": 5,
    "portata_poly": 0.05,
    "torbidita_chiarificato": 1,
    "torbidita_fango": 15,
    "umidita_fango": 5,
    "velocita_coclea": 10,
    "velocita_tamburo": 250,
}

# Simulate constant data with drift and anomalies
def simulate_sensor_data():
    # Initialize values close to the baseline
    current_values = BASELINES.copy()

    while True:
        # Generate constant sensor values with slight drift
        for key in current_values:
            # Slightly vary values around the baseline
            drift = random.uniform(-RANGES[key] / 10, RANGES[key] / 10)
            current_values[key] = max(0, current_values[key] + drift)

            # Clip to within the baseline range
            current_values[key] = max(
                BASELINES[key] - RANGES[key], 
                min(BASELINES[key] + RANGES[key], current_values[key])
            )

        # Occasionally generate anomalies
        if random.random() < 0.1:  # 10% chance of anomaly
            current_values["portata_fanghi"] = random.uniform(5, 100)
            current_values["portata_poly"] = random.uniform(-1, 1.5)
            current_values["torbidita_chiarificato"] = random.uniform(10, 20)
            current_values["torbidita_fango"] = random.uniform(200, 250)
            current_values["umidita_fango"] = random.uniform(40, 90)
            current_values["velocita_coclea"] = random.uniform(150, 200)
            current_values["velocita_tamburo"] = random.uniform(4000, 6000)

        # Get current timestamp in nanoseconds
        timestamp = int(time.time() * 1e9)

        # Write data point to InfluxDB
        point = (
            Point("dewatering_machine")
            .tag("machine_id", "machine_01")
            .field("portata_fanghi", current_values["portata_fanghi"])
            .field("portata_poly", current_values["portata_poly"])
            .field("torbidita_chiarificato", current_values["torbidita_chiarificato"])
            .field("torbidita_fango", current_values["torbidita_fango"])
            .field("umidita_fango", current_values["umidita_fango"])
            .field("velocita_coclea", current_values["velocita_coclea"])
            .field("velocita_tamburo", current_values["velocita_tamburo"])
            .time(timestamp)
        )

        write_api.write(bucket=bucket, org=org, record=point)

        # Print for verification (optional)
        print(f"{timestamp}: {point}")

        # Wait for 2 seconds
        time.sleep(2)

# Start simulation
if __name__ == "__main__":
    try:
        simulate_sensor_data()
    except KeyboardInterrupt:
        print("Simulation stopped.")
        client.close()