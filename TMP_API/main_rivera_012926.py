from dataclasses import fields

from mp_api.client import MPRester
import pandas as pd
import pickle

import string

alphabet_positions = list(enumerate(string.ascii_uppercase, start=0))
print(alphabet_positions)

# Option 1: Pass your API key directly as an argument.
with MPRester("Xh0gfyYbbnZf0C43AeQyIg5jwWESQPgq") as mpr:
        docs = mpr.materials.summary.search(
            #material_ids = ["mp-13", "mp-14", "mp-665", "mp-4014", "mp-1018027"],
            #fields = ["formula_pretty", "material_id", "elements", "density_atomic", "is_metal"]
            #fields = ["formula_pretty"]
            formula = ["BaTiO3","SrTiO3","CaTiO3", "LaMnO3", "BiFeO3", "SmFeO3", "PbTiO3",       "CaZrO3", "CaSnO3","SrZrO3","BaZrO3", "PbZrO3","BaHfO3", "SrHfO3", "CaHfO3"
                , "KNbO3", "NaNbO3", "KTaO3", "NaTaO3", "SrSnO3","BaSnO3", "CdTiO3","ZnTiO3","CaRuO3", "SrRuO3","BaRuO3", "LaCoO3", "LaNiO3", "LaCrO3", "NdFeO3"
                , "GdFeO3", "DyFeO3","LaFeO3", "TbMnO3", "DyMnO3", "EuTiO3", "YFeO3", "HoMnO3", "ErMnO3","ErMnO3", "CsPbBr3", "CsPbCl3", "CsSnI3", "CsSnI3"
                , "CsSnBr3", "FAPbBr3", "FASnI3", "MAPbCl3", "LaAlO3", "NdAlO3", "PrAlO3", "SmAlO3", "GdAlO3", "CaNbO3", "SrNbO3", "BaNbO3", "CaTaO3", "SrTaO3"
                , "BaTaO3", "CaMoO3", "SrMoO3", "BaMoO3", "CaWO3", "SrWO3", "BaWO3", "NdMnO3", "PrMnO3", "SmMnO3", "GdMnO3", "TbFeO3", "ErFeO3", "YbFeO3"
                , "CsGeI3", "CsGeBr3", "CsGeCl3", "MaSnCl3", "FASnBr3", "LaCuO3","CaCuO3", "SrCuO3", "BaPbO3", "SrIrO3", "CaIrO3"],
            #total_magnetization_normalized_vol>(0.0),
            #fields = ["formula_pretty", "structure", "lattice", "symmetry", "density_atomic", "band_gap", "is_gap_direct", "is_magnetic", "ordering", "total_magnetization", "total_magnetization_normalized_vol", "total_magnetization_normalized_formula_units", "num_magnetic_sites", "num_unique_magnetic_sites", "types_of_magnetic_species"]
        )
df = pd.DataFrame([doc.dict() for doc in docs])

#with open("perovskites_sample.pkl", "wb") as f:
#    pickle.dump(df, f)

df.to_excel("perovskites_sample_full.xlsx", index=False)

#CREAR LISTA A BASE DE UNA COLUMNA
#print(df['elements'].tolist())

print(df[['formula_pretty','total_magnetization']])


#for p in docs:
#    print(p)
#    print("-----------------------------------------------------------------------------------------------------------------------------------------------")



#elem = str(docs[0])
#elem_line = elem.splitlines()

#print(elem_line[2])
#print("--------------------------------------------------------")
#for p in elem_line:
#    print(p)



#Crear pkl file, me da un error
#print("--------------------------------------------------------")
#with open("documents.pkl", "wb") as f:
#    pickle.dump(docs, f)

#i = 0
#while i <= 2:
#    print(docs[i])
#    print("--------------------------------------------------------")
#    i = i + 1


