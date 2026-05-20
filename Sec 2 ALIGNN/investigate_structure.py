# Part 6:  Investigate a particular structure

# Let's build the graph for one of our structures and highlight a more in depth check we might do.
from evaluating_model import visualize_performance
import torch
from jarvis.core.atoms import Atoms
from alignn.graphs import Graph
import joblib
import random
from test_device import test_device

def predict_value(model, device, df, data_dir, structure_index):
    """_summary_

    Args:
        model (_type_): _description_
        device (_type_): _description_
        df (_type_): _description_
        data_dir (_type_): _description_
        structure_index (_type_): _description_

    Returns:
        _type_: _description_
    """    
    cutoff = 8.0
    model=model.to(device)
    max_neighbors = 12
    # pick one of the sample data files for this
    atoms = Atoms.from_poscar(data_dir + 'POSCAR_' + str(structure_index) + '.vasp')
    
    # We'll read back in a Manganese Oxide structure.

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

    print('Predicted normalized magnetization: ', round(out_data,3))
    print('Reference normalized magnetization: ', round(df['total_magnetization_normalized_vol'][structure_index],3))
    predicted_value = out_data
    reference_value = df['total_magnetization_normalized_vol'][structure_index]
    return atoms, predicted_value, reference_value

    # Let's apply a 1% strain to the structure, how might that affect voltage?

def apply_strain(atoms):
    """_summary_

    Args:
        atoms (_type_): _description_
    """    
    atoms_strained = atoms.strain_atoms(0.01)
    g, lg = Graph.atom_dgl_multigraph(atoms_strained)
    lat = torch.tensor(atoms_strained.lattice_mat)
    out_data = (
        model([g.to(device), lg.to(device),lat.to(device)])['out']
        .detach()
        .cpu()
        .numpy()
        .flatten()
        .tolist()[0]
    )
    print ('Predicted total magnetization: ', round(out_data,3))

# what about if we Substitute Cobalt for Manganese?

def substitute_atoms(atoms):
    """_summary_

    Args:
        atoms (_type_): _description_
    """    
    # Substitute Mn with Co
    atoms_substituted = atoms
    atoms_substituted.elements = ['Na', 'Co', 'Co', 'O', 'O', 'O', 'O']

    g, lg = Graph.atom_dgl_multigraph(atoms_substituted)
    lat = torch.tensor(atoms_substituted.lattice_mat)
    out_data = (
        model([g.to(device), lg.to(device),lat.to(device)])['out']
        .detach()
        .cpu()
        .numpy()
        .flatten()
        .tolist()[0]
    )
    print ('predicted total magnetization', round(out_data,3))

def create_df(pkl_path):
    """_summary_

    Args:
        pkl_path (_type_): _description_

    Returns:
        _type_: _description_
    """    
    df = joblib.load(pkl_path)
    return df

def test_predictions(dataset_size):
    """_summary_

    Args:
        dataset_size (_type_): _description_
    """    
    predicted_value = 0
    reference_value = 0
    error_percentage_sum = 0
    model = visualize_performance(model_dir)
    df = create_df(pkl_path)
    df_index_list = []
    total_test_sample = 0

    for i in range(dataset_size + 1):
        df_index_list.append(i)

    df["index"] = df_index_list
    df.set_index("index", drop=True, append=False, inplace=True, verify_integrity=False)
    
    for i in range(int(dataset_size*0.1)):    

        print("Test No. " + str(i))
        structure_index = random.randrange(0, dataset_size, 1)
        print("Structure index: " + str(structure_index))
        atoms, predicted_value, reference_value = predict_value(model, device, df, data_dir, structure_index)

        error_percentage = abs(predicted_value - reference_value)/reference_value
        
        print("Error percentage: " + str(error_percentage) + "%")
        error_percentage_sum = error_percentage_sum + error_percentage

        i = i + 1
        total_test_sample = i
    
    error_percentage_average = error_percentage_sum/total_test_sample
    print("Error Percentage average: " + str(error_percentage_average))


model_dir = "/home/user/Documents/Pymatgen-2026/gpu_test_clean_10ep/"
data_dir = "/home/user/Documents/Pymatgen-2026/Sec 2 ALIGNN/perovskites_data_clean/"
pkl_path = "/home/user/Documents/Pymatgen-2026/perovskites_data/perovskites_sample_clean.pkl"
dataset_size = 8901

device = test_device()
#model = visualize_performance(model_dir)
#df = create_df(pkl_path)
#atoms, predicted_value, reference_value = predict_value(model, device, df, data_dir, structure_index)
#apply_strain(atoms)
#substitute_atoms(atoms)
test_predictions(dataset_size)
    
