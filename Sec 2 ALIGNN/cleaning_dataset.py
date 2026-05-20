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
        
    """
    df = joblib.load(dataset_path)

    print(df)

    rows_to_drop = df[df["total_magnetization_normalized_vol"] == 0].index
    df2 = df.drop(rows_to_drop, inplace=False)
    
    print(df)
    print(df2)

    df.to_excel(output_dir + output_file_name + ".xlsx", index=False)
    df.to_pickle(output_dir + output_file_name + ".pkl")

dataset_path = "/home/user/Documents/Pymatgen-2026/perovskites_data/perovskites_sample.pkl"
output_dir = "/home/user/Documents/Pymatgen-2026/perovskites_data/"
output_file_name="perovskites_sample_clean_text"

cleaning_dataset(dataset_path, output_file_name, output_dir)