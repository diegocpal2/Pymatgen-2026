from mp_api.client import MPRester
import pandas as pd
from pymatgen.core import Structure
from pathlib import Path
import pickle
import joblib
import os
import torch
from alignn.models.alignn_atomwise import ALIGNNAtomWise , ALIGNNAtomWiseConfig
from jarvis.core.atoms import Atoms
from alignn.graphs import Graph
import joblib
import pandas as pd
import numpy as np
import os
from pymatgen.core import Structure, Composition
import matplotlib.pyplot as plt
import sys
from jarvis.db.jsonutils import loadjson
import pandas as pd

def material_data(pkl_opt, xlsx_opt, vasp_opt, formula):
    #CREATE MATERIAL DATA
    with MPRester("Xh0gfyYbbnZf0C43AeQyIg5jwWESQPgq") as mpr:
        docs = mpr.materials.summary.search(
            formula = formula
        )
    df = pd.DataFrame([doc.dict() for doc in docs])
    df.head()

    if pkl_opt == True:
        pkl(df)
    if xlsx_opt == True:
        xlsx(df)
    if vasp_opt == True:
        vasp(df)

def pkl(df):
    #CREATE .PKL FILE
    with open("docs.pkl", "wb") as f:
        pickle.dump(df, f)

def xlsx(df):
    #CREATE .XLSX FILE
    df.to_excel("docs.xlsx"
                "", index=False)

def vasp(df):
    #CREATE VASP FILE FOLDER FOR MATERIALS

    # Get current script directory
    current_dir = Path(__file__).parent

    # Create folder
    folder_path = current_dir / "vasp_files"
    print(folder_path)
    folder_path.mkdir(exist_ok=True)

    for i, sdict in enumerate(df["structure"]):
        structure = Structure.from_dict(sdict)   # convert dict → Structure
        os.chdir(folder_path )
        structure.to(filename=f"/home/diegop/Documents/Pymatgen-2026-Diego/Sec 2 ALIGNN/vasp_files/POSCAR_{i}.vasp", fmt="poscar")

def pkltoexcel():

    #OPEN .PKL FILE AND MAKE A .XLSX FILE (MUST BE IN PROJECT'S FOLDER)
    df = joblib.load("FILE NAME.pkl")
    df = pd.DataFrame(df) # Convert the list to a DataFrame
    df.head()
    print(df)
    df.to_excel("FILE NAME.xlsx"
                "", index=False)

create_material = True
pkl_opt = False
xlsx_opt = True
vasp_opt = True
pkltoexcel_opt = False


formula = ["BaTiO3","SrTiO3","CaTiO3", "LaMnO3", "BiFeO3", "SmFeO3", "PbTiO3",       "CaZrO3", "CaSnO3","SrZrO3","BaZrO3", "PbZrO3","BaHfO3", "SrHfO3", "CaHfO3"
                , "KNbO3", "NaNbO3", "KTaO3", "NaTaO3", "SrSnO3","BaSnO3", "CdTiO3","ZnTiO3","CaRuO3", "SrRuO3","BaRuO3", "LaCoO3", "LaNiO3", "LaCrO3", "NdFeO3"
                , "GdFeO3", "DyFeO3","LaFeO3", "TbMnO3", "DyMnO3", "EuTiO3", "YFeO3", "HoMnO3", "ErMnO3","ErMnO3", "CsPbBr3", "CsPbCl3", "CsSnI3", "CsSnI3"
                , "CsSnBr3", "FAPbBr3", "FASnI3", "MAPbCl3", "LaAlO3", "NdAlO3", "PrAlO3", "SmAlO3", "GdAlO3", "CaNbO3", "SrNbO3", "BaNbO3", "CaTaO3", "SrTaO3"
                , "BaTaO3", "CaMoO3", "SrMoO3", "BaMoO3", "CaWO3", "SrWO3", "BaWO3", "NdMnO3", "PrMnO3", "SmMnO3", "GdMnO3", "TbFeO3", "ErFeO3", "YbFeO3"
                , "CsGeI3", "CsGeBr3", "CsGeCl3", "MaSnCl3", "FASnBr3", "LaCuO3","CaCuO3", "SrCuO3", "BaPbO3", "SrIrO3", "CaIrO3"]

'''
if create_material == True:
    material_data(pkl_opt, xlsx_opt, vasp_opt, formula)

if pkltoexcel_opt == True:
    pkltoexcel()
'''

# **TMS 2025 AI Workshop: Ryan Jacobs, Ben Afflerbach, Dane Morgan (UW-Madison)**


# **TMS 2025 AI Workshop: Ryan Jacobs, Ben Afflerbach, Dane Morgan (UW-Madison)*
## Google Colab notebook demo of structure based property prediction:
## Fine tuning for prediction Na-battery material voltage

# Part 1: Installation and setup

# To begin, we need to install needed python dependencies to run [ALIGNN](https://github.com/usnistgov/alignn)

# pip install alignn

# pip install pymatgen mp_api

# Part 2: Training and Predicting using sample POSCAR data

# ALIGNN github package comes with an example dataset. let's do a quick test with that to check things are working and installed correctly

# The example data we'll work with is configured as a directory of POSCAR files. Additionally it must contain a file "id_prop.csv" which is a two two column csv with file names matching the POSCAR files paired with the property value of interest. The example dataset is a set of Band Gap values.

# The last file in the sample data folder is config_example.json

# This configuration file sets various aspects of the dataset from model architecture details, to training parameters.

# To interact with it I'll suggest double clicking from the file explorer on the left of the Google Colab interface to inspect and view directly rather than reading in the json file to Python

# To use the trained model we can load model checkpoints from the output directory

data_directory = "/home/diegop/Documents/Pymatgen-2026/alignn/alignn/examples/sample_data"
output_directory = 'sample_test/'
output_features =  1
filename = os.path.join(output_directory,'best_model.pt')
device = "cpu"
if torch.cuda.is_available():
    device = torch.device("cuda")

def use_trained_model():
    from jarvis.db.jsonutils import loadjson
    # load config from output folder
    config=loadjson(os.path.join(output_directory,'config.json'))

    model = ALIGNNAtomWise(ALIGNNAtomWiseConfig(**config["model"]))
    model.load_state_dict(torch.load(filename, map_location=device))
    model.eval()
    return model

# To make predictions we load a POSCAR file and build a graph representation

def graph_representation(model):
    cutoff = 8.0
    model=model.to(device)
    max_neighbors = 12
    # pick one of the sample data files for this quick demo
    atoms = Atoms.from_poscar("/home/diegop/Documents/Pymatgen-2026/alignn/alignn/examples/sample_data/POSCAR-JVASP-10.vasp")
    g, lg = Graph.atom_dgl_multigraph(atoms, cutoff=float(cutoff), max_neighbors=max_neighbors)
    lat = torch.tensor(atoms.lattice_mat)
    out_data = (
        model([g.to(device), lg.to(device),lat.to(device)])['out']
        .detach()
        .cpu()
        .numpy()
        .flatten()
        .tolist()[0]
    )

    print ('output: ', out_data)
    return atoms

# With the small training dataset the example model is clearly giving some unphysical values for bandgaps, but at least shows that the training scripts are working without error.
# We can also modify structures, rebuild the graph, and update predictions. In this case we make a supercell of the previous structure

def modify_structures(atoms):
    atoms = atoms.make_supercell([2, 2, 2])
    g, lg = Graph.atom_dgl_multigraph(atoms)
    lat = torch.tensor(atoms.lattice_mat)
    out_data = (
        model([g.to(device), lg.to(device),lat.to(device)])['out']
        .detach()
        .cpu()
        .numpy()
        .flatten()
        .tolist()[0]
    )
    print("supercell", out_data)

# In addition to individual structures, let's look at the model performance across the test dataset

def model_performance():
    d=loadjson(os.path.join(output_directory,'Test_results.json'))
    x=[i['target_out'][0] for i in d]
    y=[i['pred_out'] for i in d]
    ids=[i['id'] for i in d]
    
    # we can convert to csv for later

    # Create a DataFrame to save the results in csv for later
    data = {'id': ids, 'target': x, 'prediction': y}
    temp_df = pd.DataFrame(data)

    # Save the DataFrame as a CSV file
    csv_file = 'sample_test/prediction_results_test_set.csv'
    temp_df.to_csv(csv_file, index=False)

def create_plot():
    import matplotlib.pyplot as plt

    d=loadjson(os.path.join(output_directory,'Test_results.json'))
    x=[i['target_out'][0] for i in d]
    y=[i['pred_out'] for i in d]

    plt.plot(x,y,'.')
    plt.plot(x,x)
    plt.xlabel('DFT')
    plt.ylabel('ALIGNN')
    plt.savefig('DFT_ALIGNN.png', dpi=300, bbox_inches='tight')

    from sklearn.metrics import mean_absolute_error
    print('MAE',mean_absolute_error(x,y))

# Part 3: Obtaining Voltage Data
#The data file contains U-MLIP relaxed structures and average voltages for 2288 materials. Let's plot a histogram of the computed average voltages to see their distribution:

def create_df():
    d = "/home/diegop/Documents/Pymatgen-2026/Sec 2 ALIGNN"
    df = joblib.load(os.path.join(d, 'mp_Na_eqV2.pkl'))
    return df

def plot_voltage_histogram(df, dataset='MP', ion='Na'):
    bins = np.arange(0, 10, 0.2)

    # Matterverse avg voltage has a bunch of negative values- remove them!
    df = df[df['Average voltage (V/ion)'] >=0]

    plt.clf()

    plt.hist(bins=bins, x=df['Average voltage (V/ion)'], color='red', edgecolor='black', alpha=0.5, label='EquiformerV2')

    plt.xlabel('Average voltage (V/Na)', fontsize=14)
    plt.xticks(fontsize=12)
    plt.ylabel('Number of occurrences', fontsize=14)
    plt.yticks(fontsize=12)
    plt.legend(loc='best')
    plt.savefig('Voltage_histogram_'+dataset+'_'+ion+'.png', dpi=300, bbox_inches='tight')

    vals = df['Average voltage (V/ion)']
    print('EquiformerV2 stats')
    print(np.mean(vals), np.std(vals), min(vals), max(vals))

    return

model = use_trained_model()
atoms = graph_representation(model)
modify_structures(atoms)
model_performance()
create_plot()
df = create_df()
plot_voltage_histogram(df)

