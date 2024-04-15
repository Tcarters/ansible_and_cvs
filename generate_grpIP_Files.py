# this code take a csv file and generate
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
        # ip = row['Ip']
        ip = row['Ip'].strip("'")  # Strip single quotes from IP if necessary
        hostname = row['Hostname']
        
        # Check if the group already exists in the dictionary
        if group in groups:
            # Append the hostname to the existing group's list if not already present
            if (hostname, ip)  not in groups[group]:
                groups[group].append((hostname, ip))
        else:
            # Create a new entry in the dictionary with the group as the key
            groups[group] = [ (hostname, ip) ]

# Convert the dictionary to the desired list format for YAML
yaml_list = [{'groupname': group, 'members': members} for group, members in groups.items()]

# generate csv file based on the groupname in the list

for item in yaml_list:
    print (item)
    filename= item['groupname']
    filecontent = item['members']
    
    # Create individual csv file
    with open (f'./ipgroups/{filename}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        field = ["Hostname", "IpAddress"]
        
        # Write the header row
        writer.writerow(field)
         # Write the member data
        for hostname, ip in filecontent:
            writer.writerow([hostname, ip])
    # file.close()

# Define the path for the YAML file
yaml_file_path = './ipgroups/grpnameLists.yaml'

# Write to the YAML file
with open(yaml_file_path, 'w') as file:
    yaml.safe_dump(yaml_list, file, default_flow_style=False)

print(f"Groups have been successfully written to {yaml_file_path}")
