### This script converts CSV file 'dati_macchina.csv' to InfluxDB Line Protocol format.

import csv
from collections import defaultdict
from datetime import datetime

# Define machine details
machines = {
    "69h610c321e42a5fea0fc080": {"latitude": 43.1411948, "longitude": 13.067705699},
    "65f850b321e42e5ffa7cf088": {"latitude": 43.13954324, "longitude": 13.068663596},
}

# Define list of possible measurements
measurements = [
    "PV10_GiriDifferenziali", "PV02_GiriMinutoCoclea", "PV04_AssorbimentoDecanter", "PV03_Pressione",
    "PV07_Vibrazioni", "PV01_GiriMinutoTamburo", "PV08_TempCuscinetto1In", "PV09_TempCuscinetto1Out",
    "PV06_MisuratorePortataPoly", "PV05_MisuratorePortataFanghi", "PV17_UmiditàUscitaFango",
    "PV16_TorbiditàChiarificato", "PV15_TorbiditàFango", "PV34_MisuraLivelli", "PV35_ConcentrazionePoly",
    "PV31_AssorbimentoCorrenteImpianto", "PV28_PotenzaIstantaneaImpianto", "PV29_ConsumoEnergeticoImpianto"
]

# Function to process the CSV file and generate the line protocol format
def process_csv_to_line_protocol(input_file, output_file):
    # Read the CSV file and group data by timestamp
    data_by_timestamp = defaultdict(lambda: defaultdict(dict))
    
    with open(input_file, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        
        for row in csvreader:
            id_macchina = row['id_macchina']
            timestamp = int(datetime.strptime(row['data_registrazione'], '%Y-%m-%dT%H:%M:%S.%fZ').timestamp() * 1e9)  # Convert to nanoseconds
            valore = float(row['valore']) if row['valore'] else 0.0  # Convert the value to float
            nome_parametro = row['nome_parametro']
            
            # Skip if the parameter is not in the measurements list
            if nome_parametro not in measurements:
                continue
            
            # Prepare the data for this row
            data_by_timestamp[timestamp][id_macchina][nome_parametro] = valore

    # Write the formatted line protocol data to the output file
    with open(output_file, 'w') as outfile:
        for timestamp, machines_data in sorted(data_by_timestamp.items()):
            for id_macchina, fields in machines_data.items():
                # Get machine coordinates
                latitude = machines[id_macchina]["latitude"]
                longitude = machines[id_macchina]["longitude"]
                
                # Prepare the tags and fields for the line protocol
                tags = f"id_macchina={id_macchina}"
                fields_str = ",".join([f"{param}={value}" for param, value in fields.items()])
                fields_str += f",latitude={latitude},longitude={longitude}"

                # Write the line protocol format
                outfile.write(f"machine_data,{tags} {fields_str} {timestamp}\n")

# Input and output file names
input_file = 'datasets/dati_macchina.csv'
output_file = 'data/machine_data.lp'

# Call the function to process the CSV and create the new line protocol file
process_csv_to_line_protocol(input_file, output_file)

print(f"Line protocol data written to {output_file}")