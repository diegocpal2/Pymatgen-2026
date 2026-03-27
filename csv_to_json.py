import csv
import json

with open('/home/diegop/Documents/Pymatgen-2026/alignn/alignn/examples/sample_data/id_prop.csv', mode='r', newline='', encoding='utf-8') as csvfile:
    data = list(csv.DictReader(csvfile))

with open('/home/diegop/Documents/Pymatgen-2026/alignn/alignn/examples/sample_data/id_prop.json', mode='w', encoding='utf-8') as jsonfile:
    json.dump(data, jsonfile, indent=4)