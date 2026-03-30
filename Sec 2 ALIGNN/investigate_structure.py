# Part 6:  Investigate a particular structure

# Let's build the graph for one of our structures and highlight a more in depth check we might do.
from evaluating_model import visualize_performance
from train_sample_data import create_df
import torch
from jarvis.core.atoms import Atoms
from alignn.graphs import Graph


def build_graph(model, device, df):

    cutoff = 8.0
    model=model.to(device)
    max_neighbors = 12
    # pick one of the sample data files for this
    atoms = Atoms.from_poscar('/home/diegop/Documents/Pymatgen-2026/Sec 2 ALIGNN/voltage_data/POSCAR_0.vasp')
    
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

    print ('predicted Average Voltage (V/ion): ', round(out_data,3))
    print('Reference Average Voltage (V/ion): ', round(df['Average voltage (V/ion)'][0],3))
    return atoms

    # Let's apply a 1% strain to the structure, how might that affect voltage?

def apply_strain(atoms):
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
    print ('predicted Average Voltage (V/ion): ', round(out_data,3))

# what about if we Substitute Cobalt for Manganese?

def substitute_atoms(atoms):
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
    print ('predicted Average Voltage (V/ion): ', round(out_data,3))

device = "cpu"

model = visualize_performance()
df = create_df()
atoms = build_graph(model, device, df)
apply_strain(atoms)
substitute_atoms(atoms)
    
