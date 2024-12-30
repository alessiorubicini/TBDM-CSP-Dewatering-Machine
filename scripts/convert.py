import csv
import os
from datetime import datetime

# Define the directory containing your CSV files
csv_directory = 'datasets'  # Update with your directory path

# Define the output directory for Line Protocol files
output_directory = 'data'  # Update with your output directory path

# List of CSV file names to process
csv_files = [
    'umidita_fango.csv', 
    'velocita_coclea.csv', 
    'velocita_tamburo.csv', 
    'portata_fanghi.csv',
    'torbidita_fango.csv',
    'portata_poly.csv',
    'torbidita_chiarificato.csv'
]

# Function to convert CSV data to Line Protocol format
def convert_csv_to_line_protocol(csv_file):
    # Determine the measurement name based on the CSV file
    measurement_name = csv_file.split('.')[0]
    
    # Open the CSV file and process each row
    line_protocol_data = []
    with open(os.path.join(csv_directory, csv_file), mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Extract the value and timestamp
            timestamp = row['data_registrazione']
            value = row['\ufeff"valore"'].strip()  # Get the value, remove any extra spaces
            
            
            # Check if the value contains a unit and remove it (e.g., '%' or 'rpm')
            if "%" in value:
                value = value.replace("%", "").strip()
            elif "rpm" in value:
                value = value.replace("rpm", "").strip()
            elif "m3/h" in value:
                value = value.replace("m3/h", "").strip()
            elif "g/l" in value:
                value = value.replace("g/l", "").strip()

            # Convert the timestamp to InfluxDB-compatible format (RFC3339)
            #timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            #timestamp_str = timestamp.isoformat() + "Z"
            
			 # Ensure the value is numeric (float) for proper uploading to InfluxDB
            try:
                value = float(value)
            except ValueError:
                print(f"Skipping invalid value: {row['valore']} in file {csv_file}")
                continue

            # Convert the timestamp to Unix timestamp (seconds since epoch)
            try:
                timestamp_obj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                unix_timestamp_seconds = int(timestamp_obj.timestamp())  # Convert to Unix timestamp
                unix_timestamp_ns = int(unix_timestamp_seconds * 1e9)  # Convert to nanoseconds
            except ValueError:
                print(f"Skipping invalid timestamp: {timestamp} in file {csv_file}")
                continue

            # Construct the Line Protocol string
            line_protocol = f"{measurement_name},sensor={measurement_name} value={value} {unix_timestamp_ns}"
            line_protocol_data.append(line_protocol)
    
    return line_protocol_data

# Function to write Line Protocol data to a file
def write_line_protocol_to_file(output_file, line_protocol_data):
    with open(output_file, 'w') as file:
        for line in line_protocol_data:
            file.write(f"{line}\n")

# Process each CSV file and convert it to Line Protocol
for csv_file in csv_files:
    print(f"Processing file: {csv_file}")
    
    # Convert CSV to Line Protocol
    line_protocol_data = convert_csv_to_line_protocol(csv_file)
    
    # Define the output file path
    output_file = os.path.join(output_directory, f"{csv_file.split('.')[0]}.lp")
    
    # Write the Line Protocol data to the output file
    write_line_protocol_to_file(output_file, line_protocol_data)
    print(f"Line Protocol data written to: {output_file}")

print("CSV to Line Protocol conversion completed.")