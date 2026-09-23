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
import sys

def visualize_performance(model_dir):
    """
        Allows to evaluate a model's performance, generating a MAE value and a graph showing the aligning of the ALIGNN-trained-model predicted values for a specific property and the reference values included in the testing part of the dataset.

    Args:
        model_dir (string): Path of the directory containing the output of a trained model using the ALIGNN library.

    Returns:
        ALIGNN_model: Copy of the same model that was recovered from the model_dir directory path.
    """    

    output_features =  1
    filename = model_dir + 'best_model.pt'
    device = "cpu"
    if torch.cuda.is_available():
        device = torch.device("cuda")

    # load config from output folder
    config=loadjson(model_dir + '/config.json')

    model = ALIGNNAtomWise(ALIGNNAtomWiseConfig(**config["model"]))
    print(type(model))
    model.load_state_dict(torch.load(filename, map_location=device))
    model.eval()
    return model

# again load back in the test data

def load_test_data(model_dir):
    """
        Loads a model trained with the ALIGNN library and saves a plot comparing the predicted property values by the model with the reference values present in the test dataset.

    Args:
        model_dir (string): Path of the directory containing the output of a trained model using the ALIGNN library.
    """    
    d=loadjson(model_dir + '/Test_results.json')
    x=[i['target_out'][0] for i in d]
    y=[i['pred_out'] for i in d]
    ids=[i['id'] for i in d]

    # Create a DataFrame
    data = {'id': ids, 'target': x, 'prediction': y}
    voltage_df = pd.DataFrame(data)

    # Save the DataFrame as a CSV file
    csv_file = model_dir + '/prediction_results_test_set.csv'
    voltage_df.to_csv(csv_file, index=False)

    import matplotlib.pyplot as plt
    plt.plot(x,y,'.')
    plt.plot(x,x)
    plt.xlabel('Band Gap (eV)')
    plt.ylabel('ALIGNN')
    plt.savefig(sys.argv[1:][1] + ".png", dpi=600, bbox_inches='tight')

    print("A plot picture was saved with the name " + sys.argv[1:][1] + ".png")

    from sklearn.metrics import mean_absolute_error
    print('MAE',mean_absolute_error(x,y))

#model_dir = "/home/user/Documents/Pymatgen-2026/gpu_test_clean_100ep/"

#visualize_performance(model_dir)
load_test_data(sys.argv[1:][0])
#test_device()
