from test_device import test_device
from evaluating_model import visualize_performance
import torch
from jarvis.core.atoms import Atoms
from alignn.graphs import Graph
import joblib
import random

def predict_property_value(model, property_value_file, vasp_file, property):
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

    device = test_device()

    cutoff = 8.0
    model=model.to(device)
    max_neighbors = 12
    # pick one of the sample data files for this
    atoms = Atoms.from_poscar(vasp_file + '.vasp')
    
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
    
    property_value_file = property_value_file + ".txt"
    reference_property = property_value_file.readline()

    print('Predicted ' + property + ': ', round(out_data,3))
    print('Reference ' + property + ': ', round(reference_property,3))

    return atoms, predicted_value, reference_value

predict_property_value(sys.argv[1:][0], sys.argv[1:][1], sys.argv[1:][2], sys.argv[1:][3])