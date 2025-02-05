### This script simulates constant sensor data with slight variations and occasional anomalies, and writes it to InfluxDB.

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

# Simulate constant data with slight variations and occasional anomalies
def simulate_sensor_data():
	while True:
		# Generate constant sensor values with slight variations
		portata_fanghi = random.uniform(5, 50)  # Flow in m³/h
		portata_poly = random.uniform(0.05, 0.5)  # Polyelectrolyte flow in L/h
		torbidita_chiarificato = random.uniform(0, 5)  # Water turbidity in NTU
		torbidita_fango = random.uniform(20, 150)  # Sludge turbidity in NTU
		umidita_fango = random.uniform(60, 85)  # Moisture percentage
		velocita_coclea = random.uniform(20, 120)  # Screw speed in RPM
		velocita_tamburo = random.uniform(1500, 4000)  # Drum speed in RPM

		# Occasionally generate anomalies
		if random.random() < 0.2:  # 20% chance of anomaly
			portata_fanghi = random.uniform(-10, 100) if random.random() < 0.5 else random.uniform(70, 100)
			portata_poly = random.uniform(-1, 2) if random.random() < 0.5 else random.uniform(1, 2)
			torbidita_chiarificato = random.uniform(10, 20)
			torbidita_fango = random.uniform(-10, 250) if random.random() < 0.5 else random.uniform(200, 250)
			umidita_fango = random.uniform(40, 100) if random.random() < 0.5 else random.uniform(90, 100)
			velocita_coclea = random.uniform(-10, 200) if random.random() < 0.5 else random.uniform(150, 200)
			velocita_tamburo = random.uniform(500, 6000) if random.random() < 0.5 else random.uniform(5000, 6000)

		# Get current timestamp in nanoseconds
		timestamp = int(time.time() * 1e9)

		# Write data point to InfluxDB
		point = (
			Point("dewatering_machine")
			.tag("machine_id", "machine_01")
			.field("portata_fanghi", portata_fanghi)
			.field("portata_poly", portata_poly)
			.field("torbidita_chiarificato", torbidita_chiarificato)
			.field("torbidita_fango", torbidita_fango)
			.field("umidita_fango", umidita_fango)
			.field("velocita_coclea", velocita_coclea)
			.field("velocita_tamburo", velocita_tamburo)
			.time(timestamp)
		)
		
		#write_api.write(bucket=bucket, org=org, record=point)

		# Print for verification (optional)
		print(f"{timestamp}: {point}")

		# Wait for 5 seconds
		time.sleep(2)

# Start simulation
if __name__ == "__main__":
	try:
		simulate_sensor_data()
	except KeyboardInterrupt:
		print("Simulation stopped.")
		client.close()
