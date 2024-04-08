import csv
import yaml

# Path to your CSV file
csv_file_path = 'sample_ip.csv'

# Initialize an empty dictionary to store the groups and hostnames
groups = {}

# Open and read the CSV file
with open(csv_file_path, mode='r') as file:
    # Create a CSV reader object
    csv_reader = csv.DictReader(file)
    
    # Iterate over each row in the CSV file
    for row in csv_reader:
        group = row['Group']
        hostname = row['Hostname']
        
        # Check if the group already exists in the dictionary
        if group in groups:
            # Append the hostname to the existing group's list if not already present
            if hostname not in groups[group]:
                groups[group].append(hostname)
        else:
            # Create a new entry in the dictionary with the group as the key
            groups[group] = [hostname]

# Convert the dictionary to the desired list format for YAML
yaml_list = [{'groupname': group, 'members': members} for group, members in groups.items()]

# Define the path for the YAML file
yaml_file_path = 'groups.yaml'

# Write to the YAML file
with open(yaml_file_path, 'w') as file:
    yaml.dump(yaml_list, file, default_flow_style=False)

print(f"Groups have been successfully written to {yaml_file_path}")
