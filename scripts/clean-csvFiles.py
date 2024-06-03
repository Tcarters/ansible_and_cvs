import csv, sys

def validate_csv(file_path):
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        errors = []
        for row in reader:
            if len(row) != 2:
                errors.append("Invalid number of columns in row: {}".format(row))
                continue
            hostname, ip_address = row
            # if not validate_hostname(hostname):
            #     errors.append("Invalid hostname: {}".format(hostname))
            #     continue
            if not validate_ip_address(ip_address):
                errors.append("Invalid IP address: {}".format(ip_address))
                continue
        if errors:
            raise ValueError("CSV file contains errors: {}".format(errors))

def validate_hostname(hostname):
    if not hostname:
        return False
    if len(hostname) < 1 or len(hostname) > 255:
        return False
    if hostname[0] == '-' or hostname[-1] == '-':
        return False
    for char in hostname:
        if not char.isalnum() and char != '-':
            return False
    return True

def validate_ip_address(ip_address):
    parts = ip_address.split('/')
    if len(parts) != 2:
        return False
    ip, subnet_mask = parts
    octets = ip.split('.')
    if len(octets) != 4:
        return False
    for octet in octets:
        if not octet.isdigit():
            return False
        if int(octet) < 0 or int(octet) > 255:
            return False
    if not subnet_mask.isdigit():
        return False
    if int(subnet_mask) < 0 or int(subnet_mask) > 32:
        return False
    return True

# Example usage
file_path = sys.argv[1]
try:
    validate_csv(file_path)
    print("CSV file is valid")
except ValueError as e:
    print("Error: {}".format(e))
    sys.exit(1)
