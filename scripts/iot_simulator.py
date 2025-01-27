### This script simulates sensor data and writes it to InfluxDB.

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

# Simulate data
def simulate_sensor_data():
	while True:
		# Generate random sensor values
		vibration = random.uniform(0.1, 10.0)  # Vibration in m/s²
		moisture = random.uniform(30.0, 50.0)  # Moisture percentage
		screw_speed = random.uniform(100, 500)  # Screw speed in RPM
		drum_speed = random.uniform(50, 300)  # Drum speed in RPM
		sludge_flow = random.uniform(1.0, 10.0)  # Flow in m³/h
		sludge_turbidity = random.uniform(100, 500)  # Turbidity in NTU
		poly_flow = random.uniform(0, 5.0)  # Polyelectrolyte flow in L/h
		water_turbidity = random.uniform(10, 50)  # Water turbidity in NTU

		# Get current timestamp in nanoseconds
		timestamp = int(time.time() * 1e9)

		# Write data point to InfluxDB
		point = (
			Point("dewatering_machine")
			.tag("machine_id", "machine_01")
			.field("vibration", vibration)
			.field("moisture", moisture)
			.field("screw_speed", screw_speed)
			.field("drum_speed", drum_speed)
			.field("sludge_flow", sludge_flow)
			.field("sludge_turbidity", sludge_turbidity)
			.field("poly_flow", poly_flow)
			.field("water_turbidity", water_turbidity)
			.time(timestamp)
		)
		
		write_api.write(bucket=bucket, org=org, record=point)

		# Print for verification (optional)
		print(f"{timestamp}: {point}")

		# Wait for 5 seconds
		time.sleep(5)

# Start simulation
if __name__ == "__main__":
	try:
		simulate_sensor_data()
	except KeyboardInterrupt:
		print("Simulation stopped.")
		client.close()