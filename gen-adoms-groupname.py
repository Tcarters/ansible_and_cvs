import os
import yaml
import csv

def parse_yaml_file(filepath):
    """ Parse the YAML file to extract 'adom', 'devicename', and 'vdom' from each device entry. """
    with open(filepath, 'r') as file:
        data = yaml.safe_load(file)
        return [(device['adom'], device['devicename'], device['policy_pkg'], device['vdom'], ) for device in data['devices']]

def process_directory(directory):
    """ Process each subdirectory in the given directory and match YAML and CSV files. """
    results = [] # {}

    # Traverse through each subdirectory in the given directory
    for subdir, dirs, files in os.walk(directory):
        files_by_basename = {}

        # Group files by their basename
        for file in files:
            basename, ext = os.path.splitext(file)
            if basename not in files_by_basename:
                files_by_basename[basename] = []
            files_by_basename[basename].append(file)

        # Process each matched pair of YAML and CSV files
        for basename, files in files_by_basename.items():
            yaml_file = None
            csv_file = None

            # Identify YAML and CSV files by extension
            for file in files:
                if file.endswith('.yaml') or file.endswith('.yml'):
                    yaml_file = os.path.join(subdir, file)
                elif file.endswith('.csv'):
                    csv_file = os.path.join(subdir, file)

            # If both files are found, parse them and aggregate the information
            if yaml_file and csv_file:
                adom_device_vdoms = parse_yaml_file(yaml_file)
                groupname = basename  # The CSV filename without extension is the groupname

                # for adom, devicename, vdom in adom_device_vdoms:
                #     key = (adom, groupname)
                #     if key not in results:
                #         results[key] = []
                #     results[key].append({'devicename': devicename, 'vdom': vdom})
                for adom, devicename, policy, vdom in adom_device_vdoms:
                    results.append({
                        'groupname': groupname,
                        'adom': adom,
                        'devicename': devicename,
                        'policy_pkg': policy,
                        'vdom': vdom
                    })

    return results

def main():
    directory = 'ipgroups'  # Directory containing the 'ipgroups' folder
    results = process_directory(directory)

    print ( results )
   
     # Write the results to a YAML file
    with open('results/grouped-adoms-devices.yml', 'w') as outfile:
        yaml.safe_dump({'data': results}, outfile, default_flow_style=False)

    print("Data has been written to output.yml")

if __name__ == "__main__":
    main()
