import csv
import yaml
from collections import defaultdict

# Path to your CSV file
csv_file_path = 'sample_ip.csv'

# Initialize a dictionary using defaultdict to store the groups and hostnames
groups = defaultdict(list)

# Open and read the CSV file
with open(csv_file_path, mode='r', newline='') as file:
    # Create a CSV reader object
    csv_reader = csv.DictReader(file)
    
    # Iterate over each row in the CSV file
    for row in csv_reader:
        group = row['Group']
        ip = row['Ip']
        hostname = row['Hostname']
        
        # Append the hostname and IP to the existing group's list
        groups[group].append({'Hostname': hostname, 'IpAddress': ip})

# Convert the dictionary to the desired list format for YAML
yaml_list = [{'groupname': group, 'members': members} for group, members in groups.items()]

# Ensure the directory exists (create if it doesn't)
import os
if not os.path.exists('./ipgroups/'):
    os.makedirs('./ipgroups/')
    
# Define the path for the YAML file
yaml_file_path = './ipgroups/grouped_data.yaml'

# Write to the YAML file
with open(yaml_file_path, 'w') as file:
    yaml.dump(yaml_list, file, default_flow_style=False, sort_keys=False)

print(f"Group data has been successfully written to {yaml_file_path}")

# Generate CSV files based on the group name in the list
for item in yaml_list:
    filename = item['groupname']
    filecontent = item['members']
    
    # Create individual CSV file for each group
    with open(f'./ipgroups/{filename}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Hostname", "IpAddress"])  # Write the header row
        for member in filecontent:
            writer.writerow([member['Hostname'], member['IpAddress']])

print("CSV files have been successfully created for each group.")