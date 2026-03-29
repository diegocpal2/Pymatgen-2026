# Part 4: Creating the input data structure
# ALIGNN expects a set of input POSCAR files so let's create a new directory and output all 2,288 structures to POSCAR files

import joblib
import os

d = "/home/diegop/Documents/Pymatgen-2026/Sec 2 ALIGNN/"
output_dir = "/home/diegop/Documents/Pymatgen-2026/Sec 2 ALIGNN/vasp_output"

def create_vasp_directory(df):
    
    # Create the directory if it doesn't exist
    output_dir = 'voltage_data'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Create a list to store the filenames
    filenames = []

    # Iterate through the DataFrame and save each structure as a POSCAR file
    for i, structure in enumerate(df['Structure']):
        filename = f'POSCAR_{i}.vasp'
        structure.to(os.path.join(output_dir,filename))
        filenames.append(filename)

    # Add the filenames as a new column to the DataFrame
    df['poscar_filename'] = filenames

    print(f"Saved {len(df)} POSCAR files to the '{output_dir}' directory and added filenames to the DataFrame.")

# And use the previous dataframe to create our id_prop.csv

def create_csv_prop_file():
    output_file = os.path.join(output_dir, 'id_prop.csv')

    # Select the required columns and save to a CSV file without headers
    df[['poscar_filename', 'Average voltage (V/ion)']].to_csv(output_file, index=False, header=False)

    print(f"Saved id and property data to '{output_file}'.")

# The first column points to each POSCAR file we created, and the second the paired Average Voltage property
# To start we'll use the same example config file

def set_config_file():
    import os
    import shutil

    source_config_path = '/home/diegop/Documents/Pymatgen-2026/Sec 2 ALIGNN/vasp_output/config_example.json'
    destination_config_path = 'voltage_data/config.json'

    # Ensure the destination directory exists (already created in a previous step)
    output_dir = 'voltage_data'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Copy the config file
    shutil.copyfile(source_config_path, destination_config_path)

    print(f"Copied '{source_config_path}' to '{destination_config_path}'")

    from jarvis.db.jsonutils import loadjson
    import os

    config_path = 'voltage_data/config.json'
    config = loadjson(config_path)
    print("Config file loaded successfully.")
    
    return config_path, config

# And we'll make sure to update the 'filename' key which is a filename for where the constructed graphs of each structure will be cached. If we don't update this ALIGNN will continue to pull the previous structuers instead of our new ones. Anytime we want to update structures we need to make sure to clear this out or change the setting.

def clear_cache(config_path, config):
    from jarvis.db.jsonutils import dumpjson

    config['filename'] = 'V'
    print("Updated config['filename'] to:", config['filename'])

    config_path = 'voltage_data/config.json'
    dumpjson(config,config_path)
    print(f"Updated config saved to '{config_path}'")

df = joblib.load(os.path.join(d, 'mp_Na_eqV2.pkl'))

create_vasp_directory(df)
create_csv_prop_file()
config_path, config = set_config_file()
clear_cache(config_path, config)