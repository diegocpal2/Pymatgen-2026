import joblib
import pandas as pd
import numpy as np
import os
from pymatgen.core import Structure, Composition
import py3Dmol
import matplotlib.pyplot as plt

import sys
sys.path.append('mattergen')
sys.path.append('/content/mattergen')

d = '/content/drive/MyDrive/TMS AI4MSE for DEMO 2025-10-28/Sec 3 MatterGen/'
df = joblib.load(os.path.join(d, 'mp_Na_eqV2.pkl'))

# Originally used the jupyter notebook structure, wont work here
df.head()


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

# Originally used the jupyter notebook structure, may not work here
plot_voltage_histogram(df)

def show_structure_3d(struct, supercell=(1,1,1), style="ballstick", width=700, height=500, spin=False, labels=False):
    s = struct.copy()
    if supercell != (1,1,1):
        s.make_supercell(supercell)
    cif_str = s.to(fmt="cif")

    view = py3Dmol.view(width=width, height=height)
    view.addModel(cif_str, "cif")
    view.addUnitCell()
    view.setBackgroundColor("white")

    if style == "ballstick":
        view.setStyle({"sphere": {"scale": 0.23}, "stick": {"radius": 0.15}})
    elif style == "licorice":
        view.setStyle({"stick": {}})
    elif style == "vdw":
        view.setStyle({"sphere": {"scale": 0.3}})
    else:
        view.setStyle({"stick": {}})

    if labels:
        for site in s.sites:
            x, y, z = map(float, site.coords)  # cartesian Å
            view.addLabel(
                site.specie.symbol,
                {"position": {"x": x, "y": y, "z": z},
                  "fontSize": 12, "fontColor": "black",
                 "alignment": "center", "offset": {"x": 0, "y": 0},
                  "backgroundOpacity": 0.0}  # no background box
            )

    view.zoomTo()
    if spin:
        view.spin(True)
    return view.show()

# Originally used the jupyter notebook structure, may not work here
struct = df['Structure'].iloc[0]
print(struct.reduced_formula)
show_structure_3d(struct, supercell=(2, 2, 2), style="ballstick", labels=True)

# TODO STOPPED BEFORE PART 3