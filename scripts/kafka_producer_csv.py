import time
import os
import csv
from confluent_kafka import Producer
import json

# Kafka broker and topic configuration
KAFKA_BROKER = 'kafka:9092'  # Kafka broker URL (in Docker setup)
TOPIC = 'dewatering-machine'  # Kafka topic to send data to
CSV_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'data-csv')  # Path to CSV folder

# List of CSV files to read
data_files = {
    "umidita_fango": "umidita_fango.csv",
    "velocita_coclea": "velocita_coclea.csv",
    "velocita_tamburo": "velocita_tamburo.csv",
    "portata_fanghi": "portata_fanghi.csv",
    "torbidita_fango": "torbidita_fango.csv",
    "portata_poly": "portata_poly.csv",
    "torbidita_chiarificato": "torbidita_chiarificato.csv"
}

# Function to parse CSV files and extract the numerical values
def parse_csv(file_path):
    values = []
    with open(file_path, newline='') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            # Assume the value is in the first column, and it's in the format "number unit"
            value_with_unit = row[0].strip()  # Example: '4.78 m3/h'
            value = float(value_with_unit.split()[0])  # Extract the number and convert it to float
            values.append(value)
    return values

# Read all CSV files into lists
data_lists = {}
for key, file in data_files.items():
    file_path = os.path.join(CSV_FOLDER, file)
    if os.path.exists(file_path):
        data_lists[key] = parse_csv(file_path)
    else:
        raise FileNotFoundError(f"File {file_path} not found.")

# Ensure all files have the same number of rows
data_length = {key: len(data) for key, data in data_lists.items()}
if len(set(data_length.values())) > 1:
    raise ValueError("CSV files must have the same number of rows.")

# Initialize Kafka producer
producer = Producer({'bootstrap.servers': KAFKA_BROKER})

def delivery_report(err, msg):
    if err is not None:
        print(f'Error sending message: {err}')
    else:
        print(f'Message sent to {msg.topic()} [{msg.partition()}]')

def send_data_to_kafka():
    for i in range(data_length["umidita_fango"]):  # Iterate through rows
        sensor_data = {key: data_lists[key][i] for key in data_lists}
        sensor_data["timestamp"] = int(time.time() * 1e9)  # Add timestamp
        
        message_value = json.dumps(sensor_data)  # Convert to JSON
        producer.produce(TOPIC, value=message_value, callback=delivery_report)
        producer.poll(0)  # Handle async delivery reports
        
        print(f"Sent to Kafka: {message_value}")  # Debugging output
        time.sleep(2)  # Wait before sending next data point

if __name__ == "__main__":
    try:
        send_data_to_kafka()
    except KeyboardInterrupt:
        print("Simulation stopped.")
    finally:
        producer.flush()  # Ensure all messages are sent
