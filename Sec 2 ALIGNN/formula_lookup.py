import pandas as pd
from pymatgen.core import Structure, Composition
import sys

def formula_lookup(pkl_file, formula_pretty, property):
    """
        Allows for searching a specific structure formula in a given dataset contained within a .pkl file. Presents a list of all the structures found with that formula. Creates a single .vasp file of the structure selected by the user. Creates a .txt file containing the reference value associated with the selected structure.

    Args:
        pkl_file (string): Path of the .pkl file containing the dataset to be consulted.
        formula_pretty (string): Formula inputted by the user to perform a formula lookup.
        property (string): Property that's going to be consulted in the formula lookup.
    """    
    df = pd.read_pickle(pkl_file + ".pkl")
    df.set_index("formula_pretty", inplace=True)
    materials_search = df.loc[formula_pretty]

    new_index = []

    for i in range(len(materials_search)):
        new_index.append(i)
    
    materials_search.reset_index(drop=False, inplace=True)
    materials_search["index"] = new_index
    materials_search.set_index("index", inplace=True)
    search_show = materials_search.loc[:, ["formula_pretty", property]]

    #print(materials_search.loc[:, ["formula_pretty", "band_gap"]])
    print(search_show)

    selected_index = input("Select a material from the provided list (0-" + str(len(search_show) - 1) + "): ")
    vasp_file_name = input("Enter the name of the VASP file to be generated: ")
    targeted_property = input("Enter the property to be stored: ")


    sdict = materials_search["structure"].loc[materials_search.index[int(selected_index)]]
    structure = Structure.from_dict(sdict)
    structure.to(filename= f"{vasp_file_name}.vasp", fmt="poscar")

    print("The file " + vasp_file_name + ".vasp has been generated.")

    file_name = vasp_file_name + "_" + targeted_property + ".txt"

    with open(file_name, 'w') as file:
        file.write(str(materials_search[targeted_property].loc[materials_search.index[int(selected_index)]]))

    print("The file " + file_name + " has been created.")

#pkl_file = "/home/diegop/Documents/Pymatgen-2026/test_071226.pkl"
#formula_pretty = "SrTiO3"


formula_lookup(sys.argv[1:][0], sys.argv[1:][1], sys.argv[1:][2])