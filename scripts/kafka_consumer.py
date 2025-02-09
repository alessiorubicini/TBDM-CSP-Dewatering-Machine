import json
from confluent_kafka import Consumer, KafkaException, KafkaError
from influxdb_client import InfluxDBClient, Point
import time

# Kafka configuration
KAFKA_BROKER = 'localhost:9092'
TOPIC = 'dewatering-machine-live'
GROUP_ID = 'dewatering-group'

# InfluxDB configuration
INFLUXDB_URL = 'http://localhost:8086'
INFLUXDB_TOKEN = 'GpEfNAYwCGAN3Clv6sqFcL88ySgOyAoEjkpYdiEIrNKfvFg75_phdl0dL8UmkUu2WInergEK5ldKLpgd7MqI3g=='
INFLUXDB_ORG = 'Unicam'
INFLUXDB_BUCKET = 'dewatering-machine-live'

# Create a Kafka consumer instance
consumer = Consumer({
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': GROUP_ID,
    'auto.offset.reset': 'earliest'
})

# Initialize InfluxDB client
influxdb_client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = influxdb_client.write_api()

# Function to insert sensor data into InfluxDB
def insert_to_influxdb(sensor_data):
    try:
        
        point = Point("dewatering_data") \
            .tag("machine", "dewatering-machine") \
            .field("portata_fanghi", sensor_data["portata_fanghi"]) \
            .field("portata_poly", sensor_data["portata_poly"]) \
            .field("torbidita_chiarificato", sensor_data["torbidita_chiarificato"]) \
            .field("torbidita_fango", sensor_data["torbidita_fango"]) \
            .field("umidita_fango", sensor_data["umidita_fango"]) \
            .field("velocita_coclea", sensor_data["velocita_coclea"]) \
            .field("velocita_tamburo", sensor_data["velocita_tamburo"]) \
            .field("timestamp", sensor_data["timestamp"])

        
        write_api.write(INFLUXDB_BUCKET, INFLUXDB_ORG, point)
        print(f"Data inserted into InfluxDB: {sensor_data}")
        
    except Exception as e:
        print(f"Error inserting data into InfluxDB: {e}")

# Subscribe to Kafka topic
consumer.subscribe([TOPIC])

# Start consuming messages from Kafka
try:
    while True:
        # Poll Kafka for new messages
        msg = consumer.poll(timeout=1.0)  # 1-second timeout for polling

        if msg is None:
            # No new message received, continue to the next poll
            continue
        if msg.error():
            # Check for errors in consuming
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print(f"End of partition {msg.partition} reached.")
            else:
                raise KafkaException(msg.error())
        else:
            # Successfully consumed a message
            try:
                sensor_data = json.loads(msg.value().decode('utf-8'))
                insert_to_influxdb(sensor_data)  # Insert the data into InfluxDB
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON message: {e}")

except KeyboardInterrupt:
    print("Consumer interrupted. Exiting...")

finally:
    # Close the consumer and InfluxDB client
    consumer.close()
    influxdb_client.close()