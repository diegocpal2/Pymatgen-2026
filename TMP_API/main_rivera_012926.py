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
            material_ids = ["mp-13", "mp-14", "mp-665", "mp-4014", "mp-1018027"],
            fields = ["formula_pretty", "material_id", "elements", "density_atomic", "is_metal"]
        )
df = pd.DataFrame([doc.dict() for doc in docs])

with open("docs.pkl", "wb") as f:
    pickle.dump(df, f)

df.to_excel("docs.xlsx", index=False)

#CREAR LISTA A BASE DE UNA COLUMNA
#print(df['elements'].tolist())

print(df[['formula_pretty','material_id', 'elements', 'density_atomic', 'is_metal']])


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


