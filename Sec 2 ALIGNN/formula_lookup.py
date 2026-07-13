import pandas as pd
from pymatgen.core import Structure, Composition
import sys

def formula_lookup(pkl_file, formula_pretty):
    df = pd.read_pickle(pkl_file + ".pkl")
    df.set_index("formula_pretty", inplace=True)
    materials_search = df.loc[formula_pretty]

    new_index = []

    for i in range(len(materials_search)):
        new_index.append(i)
    
    materials_search.reset_index(drop=False, inplace=True)
    materials_search["index"] = new_index
    materials_search.set_index("index", inplace=True)
    search_show = materials_search.loc[:, ["formula_pretty", "band_gap"]]

    #print(materials_search.loc[:, ["formula_pretty", "band_gap"]])
    print(search_show)

    selected_index = input("Select a material from the provided list (0-" + str(len(search_show) - 1) + "): ")
    vasp_file_name = input("Enter the name of the VASP file to be generated: ")


    sdict = materials_search["structure"].loc[materials_search.index[int(selected_index)]]
    structure = Structure.from_dict(sdict)
    structure.to(filename= f"{vasp_file_name}.vasp", fmt="poscar")

    print("The file " + vasp_file_name + ".vasp has been generated.")


#pkl_file = "/home/diegop/Documents/Pymatgen-2026/test_071226.pkl"
#formula_pretty = "SrTiO3"


formula_lookup(sys.argv[1:][0], sys.argv[1:][1])
