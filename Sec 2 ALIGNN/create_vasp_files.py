# Part 4: Creating the input data structure
# ALIGNN expects a set of input POSCAR files so let's create a new directory and output all 2,288 structures to POSCAR files

import joblib
import os
from pymatgen.core import Structure, Composition
from pathlib import Path
import random
import pandas as pd
import shutil
import csv

d = "/home/diegop/Documents/Pymatgen-2026/"
output_dir = "/home/diegop/Documents/Pymatgen-2026/Sec 2 ALIGNN/perovskites_data/"
training_data_dir = "/home/diegop/Documents/Pymatgen-2026/Sec 2 ALIGNN/perovskites_training_data/"
test_data_dir = "/home/diegop/Documents/Pymatgen-2026/Sec 2 ALIGNN/perovskites_test_data/"

def create_vasp_directory(df):
    
    # Create the directory if it doesn't exist
    output_dir = 'perovskites_data'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Create a list to store the filenames
    filenames = []

    # Iterate through the DataFrame and save each structure as a POSCAR file
    for i, structure in enumerate(Structure.from_dict(df['structure'])):
        filename = f'POSCAR_{i}.vasp'
        structure.to(os.path.join(output_dir,filename))
        filenames.append(filename)

    # Add the filenames as a new column to the DataFrame
    df['poscar_filename'] = filenames

    print(f"Saved {len(df)} POSCAR files to the '{output_dir}' directory and added filenames to the DataFrame.")


def create_vasp_files(df):
    #CREATE VASP FILE FOLDER FOR MATERIALS

    # Get current script directory
    current_dir = Path(__file__).parent

    # Create a list to store the filenames
    filenames = []

    # Create folder
    folder_path = current_dir / "perovskites_data"
    print(folder_path)
    folder_path.mkdir(exist_ok=True)

    for i, sdict in enumerate(df["structure"]):
        structure = Structure.from_dict(sdict)   # convert dict → Structure
        os.chdir(folder_path )
        structure.to(filename=f"/home/diegop/Documents/Pymatgen-2026/Sec 2 ALIGNN/perovskites_data/POSCAR_{i}.vasp", fmt="poscar")
        filename = f'POSCAR_{i}.vasp'
        filenames.append(filename)
    
    # Add the filenames as a new column to the DataFrame
    df['poscar_filename'] = filenames

    return df


# And use the previous dataframe to create our id_prop.csv

def create_csv_prop_file(df, training_data_dir):
    output_file = os.path.join(training_data_dir, 'id_prop.csv')

    # Select the required columns and save to a CSV file without headers
    df[['poscar_filename', 'total_magnetization']].to_csv(output_file, index=False, header=False)

    print(f"Saved id and property data to '{output_file}'.")

# The first column points to each POSCAR file we created, and the second the paired Average Voltage property
# To start we'll use the same example config file

def set_config_file(training_data_dir):
    import os
    import shutil

    source_config_path = '/home/diegop/Documents/Pymatgen-2026/Sec 2 ALIGNN/vasp_output/config_example.json'
    destination_config_path = training_data_dir + 'config.json'

    # Ensure the destination directory exists (already created in a previous step)
    output_dir = training_data_dir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Copy the config file
    shutil.copyfile(source_config_path, destination_config_path)

    print(f"Copied '{source_config_path}' to '{destination_config_path}'")

    from jarvis.db.jsonutils import loadjson
    import os

    config_path = training_data_dir + 'config.json'
    config = loadjson(config_path)
    print("Config file loaded successfully.")
    
    return config_path, config

# And we'll make sure to update the 'filename' key which is a filename for where the constructed graphs of each structure will be cached. If we don't update this ALIGNN will continue to pull the previous structuers instead of our new ones. Anytime we want to update structures we need to make sure to clear this out or change the setting.

def clear_cache(config_path, config):
    from jarvis.db.jsonutils import dumpjson

    config['filename'] = 'V'
    print("Updated config['filename'] to:", config['filename'])

    config_path = '/home/diegop/Documents/Pymatgen-2026/Sec 2 ALIGNN/perovskites_data/config.json'
    dumpjson(config,config_path)
    print(f"Updated config saved to '{config_path}'")

def sorting_training_test_files(df):

    if not os.path.exists(training_data_dir):
        os.makedirs(training_data_dir)
    
    if not os.path.exists(test_data_dir):
        os.makedirs(test_data_dir)
    
    df = pd.read_csv("/home/diegop/Documents/Pymatgen-2026/Sec 2 ALIGNN/perovskites_data/id_prop_sorting.csv")

    for filename in df["filename"]:
        random_number = random.randrange(0, 100, 1)

        if (random_number <= 20):
            shutil.copyfile(output_dir + filename, training_data_dir + filename)
        else:
            shutil.copyfile(output_dir + filename, test_data_dir + filename)

    print("Training and test data have been sorted.")
            
def create_csv_prop_file_training_sample(df, training_data_dir):
    output_file = os.path.join(training_data_dir, 'id_prop.csv')

    poscars_filenames = []
    total_magnetization_values = []

    for i in range(df.shape[0]):
        if os.path.exists(training_data_dir + "POSCAR_" + str(i) + ".vasp"):
            poscars_filenames.append("POSCAR_" + str(i) + ".vasp")
            total_magnetization_values.append(df['total_magnetization'].loc[df.index[i]])
    i = i + 1

    # Creating a dictionary
    prop_id_columns = {'poscars_filenames': poscars_filenames, 'total_magnetization': total_magnetization_values}

    # Creating DataFrame
    df_id_prop = pd.DataFrame(prop_id_columns)

    # Saving to CSV
    df_id_prop.to_csv(training_data_dir + 'id_prop.csv', index=False, header=False)

df = joblib.load(os.path.join(d, 'perovskites_sample.pkl'))

#create_vasp_directory(df)
#df = create_vasp_files(df)
#create_csv_prop_file(df, training_data_dir)
config_path, config = set_config_file(training_data_dir)
clear_cache(config_path, config)
#sorting_training_test_files()
#create_csv_prop_file_training_sample(df, training_data_dir)