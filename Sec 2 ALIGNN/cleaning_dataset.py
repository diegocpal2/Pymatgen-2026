import joblib
import os
from pymatgen.core import Structure, Composition
from pathlib import Path
import random
import pandas as pd
import shutil
import csv
from jarvis.db.jsonutils import loadjson

def cleaning_dataset(dataset_path, output_file_name, output_dir):
    """
        Allows erasing entries in a dataset based in an specific property and value associated with that property (hard coded). 
    Args:
        dataset_path (string): Path of the .pkl file containing the dataset to be modified.
        output_file_name (string): Name of the file to be outputed containing the modified dataset.
        output_dir (string): Directory where the modified dataset .pkl and .xlsx files are going to be saved.
    """    
    df = joblib.load(dataset_path)

    print(df)

    rows_to_drop = df[df["band_gap"] == 0].index
    df2 = df.drop(rows_to_drop, inplace=False)
    
    print(df)
    print(df2)

    df2.to_excel(output_dir + output_file_name + ".xlsx", index=False)
    df2.to_pickle(output_dir + output_file_name + ".pkl")

dataset_path = "/home/user/Documents/Pymatgen-2026/perovskites_bandgap.pkl"
output_dir = "/home/user/Documents/Pymatgen-2026/"
output_file_name="perovskites_bandgap_clean"

cleaning_dataset(dataset_path, output_file_name, output_dir)