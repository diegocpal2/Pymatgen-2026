# Virtual Environment Setup for Runnin the Sec 2 ALINNG Algorithm

## Step 1: Clone the repository and the specific branch.

Type the following commands in the terminal:

<code>gh repo clone https://github.com/diegocpal2/Pymatgen-2026.git -- --branch Diego</code>

## Step 2: Open the downloaded repository on the IDE.

Use the option "Open folder" to open the "Pymatgen-2026" directory.

## Step 3: Check the git version

Type the following commands in the terminal:

<code>git checkout v2024.12.12</code>

## Step 4: Install torch 2.4 with cuda 1.24

Type the following commands in the terminal:

<code>pip install -q --no-cache-dir dgl -f https://data.dgl.ai/wheels/torch-2.4/cu124/repo.html</code>

<code>pip install -e .</code>

## Step 5: Install the pymatgen and mp_api packages

<code>pip install pymatgen mp_api</code>

## Step 6: Install the ALIGNN package

<code>git clone https://github.com/usnistgov/alignn.git</code>

# Training the sample data

## Step 1: Enter the ALIGNN library directory

Type the following commands in the terminal:

<code>cd alignn</code>

## Step 2: Train the sample data

Type the following commands in the terminal:

<code>train_alignn.py --root_dir "alignn/examples/sample_data" \
                 --epochs 10 \
                 --batch_size 16 \
                 --config "alignn/examples/sample_data/config_example.json" \
                 --output_dir="sample_test"</code>


# Training with other structure databases

## Step 1: Download the desired structures sample from the materials project database using the API method

The functions for downloading the structural data for training are included in the file <code>create_vasp_files.py</code>. The file can be configured to execute all the functions in sequence. It is necessary to already have the <code>*.pkl</code> file containing a table with the list of materials. This table must contain the <code>structure</code> column in order to be able to create the vasp files.

In order to generate the vasp structural files the <code>create_vasp_files.py</code> file must be executed with the end of the file set up in the shown manner:

<code>df = joblib.load(os.path.join(d, "pkl_file_path"))<br>
<br>
config_path = "current_directory_path" + 'Sec 2 ALIGNN/perovskites_data/config.json'<br>
d = "current_directory_path"<br>
output_dir = "trained_model_output_directory"<br>
<br>
df = create_vasp_files(df)<br>
create_csv_prop_file(df, training_data_dir)<br>
config_path, config = set_config_file(training_data_dir)<br>
clear_cache(config_path, config)
</code>

The variables <code>pkl_file_path</code>, <code>current_directory_path</code> and, <code>trained_model_output_directory</code> must be replaced by the appropriated absolute paths.

<strong>Note:</strong> For Windows based systems paths are written with "\" instead of "/" which is used in unix based systems (MacOS and Linux).

## Step 2: Train the model with the downloaded database

Execute the following command in the terminal.

<code>train_alignn.py --root_dir training_data_directory \
                --epochs number_of_epochs \
                --batch_size batch_size \
                --config config_file_path \
                --output_dir=output_directory</code>

The arguments for the file must be replaced in the following manner:

<code>training_data_directory</code>: Directory containing the generated vasp files, <code>id_prop.csv</code> and, <code>config.json</code> files.<br>  
<code>number_of_epochs</code>: Number of iterations the training algorithm is going to execute.<br>
<code>batch_size</code>:<br>
<code>config_file_path</code>: Path of the <code>config.json</code> file.<br>
<code>output_directory</code>: Name of the directory where the model files will be generated.<br>

# Making predictions with the trained models


