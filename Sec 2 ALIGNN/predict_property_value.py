from test_device import test_device
from evaluating_model import visualize_performance
import torch
from jarvis.core.atoms import Atoms
from alignn.graphs import Graph
import joblib
import random
import sys

def predict_property_value(model_dir, property_value_file, vasp_file, property):
    """
        Allows for the prediction of a specific property value using a model trained using the ALIGNN library. The function shows the the reference property value and the predicted value to permit for comparison of both values.

    Args:
        model_dir (string): Path of the trained model to be consulted.
        property_value_file (string): Path of the .txt file containing the property value. 
        vasp_file (string): Path of the structure .vasp file to allow for prediction of properties. 
        property (string): Name of the property to be used for a prediction.
        
    """    

    device = test_device()
    model = visualize_performance(model_dir + "/")

    cutoff = 8.0
    model=model.to(device)
    max_neighbors = 12
    # pick one of the sample data files for this
    atoms = Atoms.from_poscar(vasp_file)
    
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
    
    property_file = open(property_value_file, "r+")
    property_file.seek(0)

    property_value_file = property_value_file
    reference_property = property_file.readline()

    print('Predicted ' + property + ': ', round(out_data,3))
    print('Reference ' + property + ': ', round(float(reference_property),3))

    #return atoms, predicted_value, reference_value

predict_property_value(sys.argv[1:][0], sys.argv[1:][1], sys.argv[1:][2], sys.argv[1:][3])