from mp_api.client import MPRester
import pandas as pd
from pymatgen.core import Structure
from pathlib import Path
import pickle
import joblib

create_material = True
pkl_opt = True
xlsx_opt = False
vasp_opt = True
pkltoexcel_opt = False

def material_data(pkl_opt, xlsx_opt, vasp_opt):
    #CREATE MATERIAL DATA
    with MPRester("Xh0gfyYbbnZf0C43AeQyIg5jwWESQPgq") as mpr:
        docs = mpr.materials.summary.search(
            formula=["BaTiO3","SrTiO3","CaTiO3", "LaMnO3", "BiFeO3", "SmFeO3", "PbTiO3","CaZrO3", "CaSnO3","SrZrO3","BaZrO3", "PbZrO3","BaHfO3", "SrHfO3", "CaHfO3"
                , "KNbO3", "NaNbO3", "KTaO3", "NaTaO3", "SrSnO3","BaSnO3", "CdTiO3","ZnTiO3","CaRuO3", "SrRuO3","BaRuO3", "LaCoO3", "LaNiO3", "LaCrO3", "NdFeO3"
                , "GdFeO3", "DyFeO3","LaFeO3", "TbMnO3", "DyMnO3", "EuTiO3", "YFeO3", "HoMnO3", "ErMnO3","ErMnO3", "CsPbBr3", "CsPbCl3", "CsSnI3", "CsSnI3"
                , "CsSnBr3", "FAPbBr3", "FASnI3", "MAPbCl3", "LaAlO3", "NdAlO3", "PrAlO3", "SmAlO3", "GdAlO3", "CaNbO3", "SrNbO3", "BaNbO3", "CaTaO3", "SrTaO3"
                , "BaTaO3", "CaMoO3", "SrMoO3", "BaMoO3", "CaWO3", "SrWO3", "BaWO3", "NdMnO3", "PrMnO3", "SmMnO3", "GdMnO3", "TbFeO3", "ErFeO3", "YbFeO3"
                , "CsGeI3"]
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
    folder_path.mkdir(exist_ok=True)

    for i, sdict in enumerate(df["structure"]):
        structure = Structure.from_dict(sdict)   # convert dict → Structure
        structure.to(filename=f"vasp_files/POSCAR_{i}.vasp", fmt="poscar")

def pkltoexcel():

    #OPEN .PKL FILE AND MAKE A .XLSX FILE (MUST BE IN PROJECT'S FOLDER)
    df = joblib.load("FILE NAME.pkl")
    df = pd.DataFrame(df) # Convert the list to a DataFrame
    df.head()
    print(df)
    df.to_excel("FILE NAME.xlsx"
                "", index=False)

if create_material == True:
    material_data(pkl_opt, xlsx_opt, vasp_opt)

if pkltoexcel_opt == True:
    pkltoexcel()