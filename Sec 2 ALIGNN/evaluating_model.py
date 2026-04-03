'''
!train_alignn.py --root_dir 'voltage_data' \
                --epochs 10 \
                --batch_size 16 \
                --config './voltage_data/config.json' \
                --output_dir=voltage_output
'''

# Let's visualize the performance

import torch
from alignn.models.alignn_atomwise import ALIGNNAtomWise , ALIGNNAtomWiseConfig
from jarvis.db.jsonutils import loadjson
import pandas as pd

def visualize_performance(model_dir):
    
    output_features =  1
    filename = model_dir + 'best_model.pt'
    device = "cpu"
    if torch.cuda.is_available():
        device = torch.device("cuda")

    # load config from output folder
    config=loadjson(model_dir + 'config.json')

    model = ALIGNNAtomWise(ALIGNNAtomWiseConfig(**config["model"]))
    model.load_state_dict(torch.load(filename, map_location=device))
    model.eval()
    return model

# again load back in the test data

def load_test_data(model_dir):
    d=loadjson(model_dir + 'Test_results.json')
    x=[i['target_out'][0] for i in d]
    y=[i['pred_out'] for i in d]
    ids=[i['id'] for i in d]

    # Create a DataFrame
    data = {'id': ids, 'target': x, 'prediction': y}
    voltage_df = pd.DataFrame(data)

    # Save the DataFrame as a CSV file
    csv_file = model_dir + 'prediction_results_test_set.csv'
    voltage_df.to_csv(csv_file, index=False)

    import matplotlib.pyplot as plt
    plt.plot(x,y,'.')
    plt.plot(x,x)
    plt.xlabel('Total Magnetization')
    plt.ylabel('ALIGNN')
    plt.savefig('Prediction_results_perovskites.png', dpi=300, bbox_inches='tight')

    from sklearn.metrics import mean_absolute_error
    print('MAE',mean_absolute_error(x,y))

model_dir = "/home/diegop/Documents/Pymatgen-2026/perovskites_total_magnetization_full_data/"

visualize_performance(model_dir)
load_test_data(model_dir)

