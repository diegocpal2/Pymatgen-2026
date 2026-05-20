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
from jarvis.db.jsonutils import loadjson

def create_vasp_files(df, output_dir):
    """
       Creates the vasp files corresponding to a Materials Project Pandas dataframe. The dataframe must include the "structure" column. 

    Args:
        df (pandas_dataframe): Pandas dataframe containing the results of pulling a series of materials information form the The Materials Project site using their API (library mp_api). The dataframes must contain the "structure" column.
        dir_name (string): Name of the directory where the vasp files are going to be stored. The directory will be created within the current directory.

    Returns:
        df: Dataframe from the argument "df" with the added column "filenames" which contains the filenames of the vasp files created for each material in the dataframe.
    """    
    #CREATE VASP FILE FOLDER FOR MATERIALS

    # Get current script directory
    current_dir = Path(__file__).parent

    # Create a list to store the filenames
    filenames = []

    # Create folder
    try:
        os.makedirs(output_dir)
        print(f"Directory '{output_dir}' created successfully.")
    except FileExistsError:
        print(f"Directory '{output_dir}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{output_dir}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

    for i, sdict in enumerate(df["structure"]):
        structure = Structure.from_dict(sdict)   # convert dict → Structure
        os.chdir(output_dir)
        structure.to(filename= output_dir + f"POSCAR_{i}.vasp", fmt="poscar")
        filename = f'POSCAR_{i}.vasp'
        filenames.append(filename)
    
    # Add the filenames as a new column to the DataFrame
    df['poscar_filename'] = filenames

    return df


# And use the previous dataframe to create our id_prop.csv

def create_csv_prop_file(df, output_dir, mat_property):
    """
        Creates the CSV properties file in the same folder of the vasp files. This files contains two columns. The first column contains the vasp files filenames for each structure in the dataframe. The second column contains the numerical value of the property that the model is going to be trained on. The file will have the name "id_prop.csv". The file is generated without headers which is required by the functions in "train_alignn.py".   

    Args:
        df (df): Pandas dataframe containing the results of pulling a series of materials information form the The Materials Project site using their API (library mp_api). The dataframes must contain the "structure" column. This dataframe must also contain the "poscar_filenames" column, therefore it must be the one returned by the function create_vasp_files(df, dir_name).
        training_data_dir (str): Path of the directory containing the vasp files to be used for the training of the model. The CSV file "id_prop.csv" will be generated in this directory.
        mat_property (str): Property that the training of the model is going to be focused on.  
    """    
    output_file = os.path.join(output_dir, 'id_prop.csv')

    # Select the required columns and save to a CSV file without headers
    df[['poscar_filename', mat_property]].to_csv(output_file, index=False, header=False)

    print(f"Saved id and property data to '{output_file}'.")

# The first column points to each POSCAR file we created, and the second the paired Average Voltage property
# To start we'll use the same example config file

def set_config_file(source_config_path, output_dir):
    """
       Duplicates the config file "config.json" into the training data directory. This file can be edited to control certain training parameters.

    Args:
        training_data_dir (str): Path of the directory containing the vasp files to train the model. The config file "config.json" will be copied into this directory.

    Returns:
        str: Path to the copied config "config.json" file.
        dict: Dictionary containing the setup parameters for the training of the model.
    """    
    import os
    import shutil

    destination_config_path = output_dir + 'config.json'

    # Ensure the destination directory exists (already created in a previous step)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Copy the config file
    shutil.copyfile(source_config_path, destination_config_path)

    print(f"Copied '{source_config_path}' to '{destination_config_path}'")

    config_path = output_dir + 'config.json'
    config = loadjson(config_path)
    print("Config file loaded successfully.")
    
    return config_path, config

# And we'll make sure to update the 'filename' key which is a filename for where the constructed graphs of each structure will be cached. If we don't update this ALIGNN will continue to pull the previous structures instead of our new ones. Anytime we want to update structures we need to make sure to clear this out or change the setting.

def clear_cache(config_path):
    """
        Clears the filename registry in the ALIGNN library. This cache must be cleared anytime a new model is going to be trained to avoid the model being trained using previously used structures.

    Args:
        config_path (str): Path of the directory containing the vasp files and csv properties file "id_prop.csv".
        config (dict): Dictionary which contains the setup parameters for the training. This file will be used by the file "training_alignn.py".
    """    
    from jarvis.db.jsonutils import dumpjson
    
    config = loadjson(config_path)

    config['filename'] = 'V'
    print("Updated config['filename'] to:", config['filename'])

    config_path = config_path
    dumpjson(config,config_path)
    print(f"Updated config saved to '{config_path}'")


dataframe_source = "/home/user/Documents/Pymatgen-2026/perovskites_data/perovskites_sample_cleaned.pkl"
output_dir = "/home/user/Documents/Pymatgen-2026/Sec 2 ALIGNN/perovskites_data_cleaned/"
mat_property = "total_magnetization_normalized_vol"
source_config_path = "/home/user/Documents/Pymatgen-2026/alignn/alignn/examples/sample_data/config_example.json"

#d = "/home/diegop/Documents/Pymatgen-2026/perovskites_data"

#training_data_dir = "/home/diegop/Documents/Pymatgen-2026/Sec 2 ALIGNN/perovskites_training_data/"
#test_data_dir = "/home/diegop/Documents/Pymatgen-2026/Sec 2 ALIGNN/perovskites_test_data/"

#df = joblib.load(dataframe_source)
#df = create_vasp_files(df, output_dir)
#create_csv_prop_file(df, output_dir, mat_property)
config_path, config = set_config_file(source_config_path, output_dir)
clear_cache(config_path)