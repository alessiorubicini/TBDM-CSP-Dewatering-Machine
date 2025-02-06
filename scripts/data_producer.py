import time
import random
from confluent_kafka import Producer
import json

# Kafka broker and topic configuration
KAFKA_BROKER = 'kafka:9092'  # Kafka broker URL (in Docker setup)
TOPIC = 'dewatering-machine'  # Kafka topic to send data to

# Callback function to handle delivery reports (success or error)
def delivery_report(err, msg):
    if err is not None:
        print(f'Error sending message: {err}')
    else:
        print(f'Message sent to {msg.topic()} [{msg.partition()}]')

# Initialize Kafka producer
producer = Producer({'bootstrap.servers': KAFKA_BROKER})

# Simulate constant data with slight variations and occasional anomalies
def simulate_sensor_data():
    while True:
        # Generate constant sensor values with slight variations (randomly)
        portata_fanghi = random.uniform(5, 50)  # Flow rate in m³/h
        portata_poly = random.uniform(0.05, 0.5)  # Polyelectrolyte flow in L/h
        torbidita_chiarificato = random.uniform(0, 5)  # Water turbidity in NTU
        torbidita_fango = random.uniform(20, 150)  # Sludge turbidity in NTU
        umidita_fango = random.uniform(60, 85)  # Sludge moisture percentage
        velocita_coclea = random.uniform(20, 120)  # Screw speed in RPM
        velocita_tamburo = random.uniform(1500, 4000)  # Drum speed in RPM

        # Occasionally generate anomalies (20% chance)
        if random.random() < 0.2:  # 20% chance of anomaly
            portata_fanghi = random.uniform(-10, 100) if random.random() < 0.5 else random.uniform(70, 100)
            portata_poly = random.uniform(-1, 2) if random.random() < 0.5 else random.uniform(1, 2)
            torbidita_chiarificato = random.uniform(10, 20)  # Anomalous turbidity
            torbidita_fango = random.uniform(-10, 250) if random.random() < 0.5 else random.uniform(200, 250)
            umidita_fango = random.uniform(40, 100) if random.random() < 0.5 else random.uniform(90, 100)
            velocita_coclea = random.uniform(-10, 200) if random.random() < 0.5 else random.uniform(150, 200)
            velocita_tamburo = random.uniform(500, 6000) if random.random() < 0.5 else random.uniform(5000, 6000)

        # Prepare the sensor data in a dictionary (this is what will be sent to Kafka)
        sensor_data = {
            "portata_fanghi": portata_fanghi,  # Flow rate in m³/h
            "portata_poly": portata_poly,  # Polyelectrolyte flow in L/h
            "torbidita_chiarificato": torbidita_chiarificato,  # Water turbidity in NTU
            "torbidita_fango": torbidita_fango,  # Sludge turbidity in NTU
            "umidita_fango": umidita_fango,  # Sludge moisture percentage
            "velocita_coclea": velocita_coclea,  # Screw speed in RPM
            "velocita_tamburo": velocita_tamburo,  # Drum speed in RPM
            "timestamp": int(time.time() * 1e9)  # Current timestamp in nanoseconds
        }

        # Convert the sensor data dictionary to a JSON string
        message_value = json.dumps(sensor_data)

        # Send the message to Kafka topic
        producer.produce(TOPIC, value=message_value, callback=delivery_report)
        producer.poll(0)  # Poll to handle any asynchronous delivery reports

        print(f"Sent to Kafka: {message_value}")  # Print the sent message (for debugging)

        # Wait for 2 seconds before sending the next data point
        time.sleep(2)

# Start the simulation of sensor data
if __name__ == "__main__":
    try:
        simulate_sensor_data()  # Start generating and sending data
    except KeyboardInterrupt:
        print("Simulation stopped.")  # Handle manual interruption (Ctrl+C)
    finally:
        producer.flush()  # Make sure all pending messages are sent before exiting
