# Sec 2 Documentation

# Virtual environment installation instructions for Fedora Linux

## Step 1

Install Python 3.12 using the operating system's terminal:

```
sudo dnf install python3.12
```

## Step 2

Open the IDE of your preference (VS Code recommended) and use the terminal to create a virtual environment for the project:

```
python3.12 -m venv .Sec2venv
```

## Step 3

Activate the virtual environment:

```
source .Sec2venv/bin/activate
```

## Step 4

Clone the ALIGNN library from github.com, enter the downloaded folder from the terminal and check the library version:

```
git clone https://github.com/atomgptlab/alignn.git
cd alignn
git checkout v2024.12.12
```
## Step 5

Install torch (This tutorial assumes that the environment is beign setup with access to a moder Nvidia RTX GPU compatible with the latest torch and CUDA versions).

```
pip3 install torch torchvision
```

## Step 6

Install the pymatgen and The Materials Project API libraries.

```
pip install pymatgen mp_api
```

## Step 7

Install the ALIGNN library.

```
pip install -e .
```

## Step 8

Clone the Pymatgen-2026 library.

```
git clone -b Diego https://github.com/diegocpal2/Pymatgen-2026.git
```

## Step 9

Copy the Pymatgen-2026 repository files to ensure that they share the same directory with the .Sec2venv.

# Using the application

## Program execution

A commandline interface (CLI) has been created to facilitate the interaction between the user and the ALIGNN library. The file *execute_alignn.sh* can be executed entering the following command in the terminal:

```bash
./execute_alignn.sh
```

After executing the the script the user is presented with the following list of options:

```
This is an script to prepare a database materials database, train models, evaluate the trained models and make predictions.
What action are you looking to execute?
1. Download a database from The Materials Project.
2. Prepare database for training.
3. Train model.
4. Evaluate model.
5. Formula lookup.
6. Predict property value.
7. Predict property after applying strain to the structure.
8. Predict property after changing structure atoms.

Select an action (1-8):
```

This menu allows for the entering of a number 1-8 to select the action to be performed. The use of the different actions will be described in the following sections.

## 1. Download a database from The Materials Project.

To download a database from the materials project enter the number 1 after the initial menu appearance and press enter. Then, the user is presented with the following question:

```
To download a database from The Materials Project follow the instructions: 
Enter the name of the .pkl and .xlsx files following the format: file_name:\
```

The name for both files has to be entered without an extention. Then the user is presented with the following question:

```
Enter the list of elements to be downloaded following the format: element_1,element_2:
```

The formulas list shouldn't have spaces between the formulas and the commas as the example presented in the query. After entering the elements list, the user is presented with the following query:

```
Enter the fields to be downloaded following the format: field_1,field_2:
```

The fields list shouldn't have spaces between entries as shown in the example that accompanies the query. The inclusion of the properties formula_pretty and structure in the list is obligatory due to containing the information relating to the formula and the crystalline structure of the listed substances. The .pkl and .xlsk files have been saved at the project root directory.

The available properties in The Materials Project database are the following: 

'band_gap', 'origins', 'is_metal', 'possible_species', 'energy_per_atom', 'ordering', 'dos', 'dos_energy_up', 'num_magnetic_sites', 'database_IDs', 'total_magnetization_normalized_vol', 'es_source_calc_id', 'is_gap_direct', 'xas', 'dos_energy_down', 'shear_modulus', 'task_ids', 'energy_above_hull', 'density_atomic', 'elements', 'total_magnetization', 'warnings', 'property_name', 'has_reconstructed', 'shape_factor', 'formula_anonymous', 'composition', 'composition_reduced', 'symmetry', 'vbm', 'uncorrected_energy_per_atom', 'density', 'e_total', 'chemsys', 'builder_meta', 'material_id', 'weighted_work_function', 'universal_anisotropy', 'equilibrium_reaction_energy_per_atom', 'e_ionic', 'num_unique_magnetic_sites', 'theoretical', 'decomposes_to', 'grain_boundaries', 'e_electronic', 'weighted_surface_energy_EV_PER_ANG2', 'is_magnetic', 'efermi', 'homogeneous_poisson', 'has_props', 'types_of_magnetic_species', 'bulk_modulus', 'nelements', 'deprecated', 'last_updated', 'deprecation_reasons', 'is_stable', 'n', 'nsites', 'formation_energy_per_atom', 'surface_anisotropy', 'weighted_surface_energy', 'e_ij_max', 'volume', 'cbm', 'bandstructure', 'total_magnetization_normalized_formula_units'

It is important to note that only properties that consist of numeric values can be used for training with ALIGNN library.

## 2. Prepare database for training.

This option allows for setting up a downloaded database for training. To select this option the user must enter the number 2 an press enter. After selecting this option the user is presented with the following query:

```
To prepare database for training follow the instructions:
Enter the name of the .pkl file (example):
```

The name of the .pkl file must be entered without its corresponding extension. Then, the interface presents the following query:

```
Enter the name of the output directory:
```

The name of the output directory that's gonna contain the .vasp crystalline structure files, the *config.json* file, and the *id_prop.csv*. Each .vasp file corresponds to the crystalline structure of one entry in the selected .pkl table. The *config.json* file contains the setup parameters to be used during the training. The *id_prop.csv* file contains a list of each .vasp file created inside the directory accompanied by the numeric value of the property that the training of the model is going to be targeting. After entering the name of the directory and pressing enter the user is presented with the following query:

```
Enter the material property to train the model:
```

The name of the property to be used for training must be typed exactly as presented in the .pkl table. Three types of files must have been created in the new directory: .vasp files named in the format *POSCAR_0.vasp* with the number increasing with each structure added, the *config.json*, and *id_prop.csv* files.

## 3. Train model.

To activate this option the user must type "3" and press enter. This option allows for the training of a machine learning model using the ALIGNN library and the files prepared in the second menu option. After entering the menu the user encounters the following message:

```
To train the model follow the instructions:
Enter the name of the training data folder:
```

The name of the folder created using the option *2. Prepare database for training.* must be typed. After entering the information, the user is presented with the following query:

```
Enter the number of epochs for training:
```

The number of epochs to train must be typed. A number of epochs no less than 200 is recommended. Then, the program ask fo the batch size to be used:

```
Enter the batch size (4, 16, 32):
```

A batch size of 16 is recommended for local setups with 8GB graphics cards. In the next step the interface ask the user about the name of the directory where the trained model is going to be stored:

```
Enter the name of the trained model directory:
```

If the information is correct the training of the model must begin. The files stored inside the directory named on the previous step. This process can take several hours depending on the capacity of the hardware available to perform the training.

## 4. Evaluate model.

To activate this option the user must type "4" and press enter. This option allows to evaluate the performance of a trained model providing an Mean Absolute Error (MAE) value and generating a .png file containing a plot comparing the property values predicted by a trained model and the reference values contained in the testing group. After selecting this option, the user will be presented with the following instructions:

```
To evaluate a model follow the instructions
Enter the name of the model directory:
```

The name of the directory containing the model created in the previous step must be typed. The next step ask for the following:

```
Enter the name of the plot file:
```

After entering the name of the plot file the evaluation process must begin. A MAE value must have been generated and a .png file with assigned name must have been created.

## 5. Formula lookup.

To activate this option the user must type "5" and press enter. This option allows to search for an specific formula in a .pkl table file and generate a crystalline structure .vasp file and a .txt file corresponding to the numeric value of the property associated with that structure/formula. The user is presented with the following query:

```
To perform a formula lookup follow the instructions
Enter the name of the pkl file:
```

The name of the file must be typed without its extension. After entering the name corresponding to the .pkl file the user is presented with the following message:

```
Enter the formula to search:
```

The formula to search must be entered. The next steps is presented as shown:

```
Enter the name of the property to retrieve:
```

The name of the property must be typed exactly as is presented in the .pkl table. The user is presented with a list of elements corresponding to the provided formula as the one shown below:

```
formula_pretty  band_gap
index                         
0             BaTiO3    1.6675
1             BaTiO3    2.5527
2             BaTiO3    2.2934
3             BaTiO3    1.7261
4             BaTiO3    1.7237
5             BaTiO3    0.0000
6             BaTiO3    0.0000
7             BaTiO3    2.0811
8             BaTiO3    0.4807
9             BaTiO3    0.0000
10            BaTiO3    0.0000
Select a material from the provided list (0-10):
```

The user must select one the entries typing its corresponding number.

# List of python files, functions and their respective docstrings.

## cleaning_dataset.py

### cleaning_dataset()

**Summary:** Allows erasing entries in a dataset based in an specific property and value associated with that property (hard coded).

**Args:**
        
**dataset_path (string):** Path of the .pkl file containing the dataset to be modified.
        
**output_file_name (string):** Name of the file to be outputed containing the modified dataset.
        
**output_dir (string):** Directory where the modified dataset .pkl and .xlsx files are going to be saved.

## create_vasp_files.py

### create_vasp_files()

### formula_lookup()

    Summary:
       Creates the vasp files corresponding to a Materials Project Pandas dataframe. The dataframe must include the "structure" column. 

    Args:
        df (pandas_dataframe): Pandas dataframe containing the results of pulling a series of materials information form the The Materials Project site using their API (library mp_api). The dataframes must contain the "structure" column.
        dir_name (string): Name of the directory where the vasp files are going to be stored. The directory will be created within the current directory.

    Returns:
        df: Dataframe from the argument "df" with the added column "filenames" which contains the filenames of the vasp files created for each material in the dataframe.

### create_csv_prop_file()

    Summary:
        Creates the CSV properties file in the same folder of the vasp files. This files contains two columns. The first column contains the vasp files filenames for each structure in the dataframe. The second column contains the numerical value of the property that the model is going to be trained on. The file will have the name "id_prop.csv". The file is generated without headers which is required by the functions in "train_alignn.py".   

    Args:
        df (df): Pandas dataframe containing the results of pulling a series of materials information form the The Materials Project site using their API (library mp_api). The dataframes must contain the "structure" column. This dataframe must also contain the "poscar_filenames" column, therefore it must be the one returned by the function create_vasp_files(df, dir_name).
        training_data_dir (str): Path of the directory containing the vasp files to be used for the training of the model. The CSV file "id_prop.csv" will be generated in this directory.
        mat_property (str): Property that the training of the model is going to be focused on.

### set_config_file()

    Summary:
       Duplicates the config file "config.json" into the training data directory. This file can be edited to control certain training parameters.

    Args:
        training_data_dir (str): Path of the directory containing the vasp files to train the model. The config file "config.json" will be copied into this directory.

    Returns:
        str: Path to the copied config "config.json" file.
        dict: Dictionary containing the setup parameters for the training of the model.

### clear_cache()

    Summary:
        Clears the filename registry in the ALIGNN library. This cache must be cleared anytime a new model is going to be trained to avoid the model being trained using previously used structures.

    Args:
        config_path (str): Path of the directory containing the vasp files and csv properties file "id_prop.csv".
        config (dict): Dictionary which contains the setup parameters for the training. This file will be used by the file "training_alignn.py".

## evaluating_model.py

### visualize_performance()

    Summary:
        Allows to evaluate a model's performance, generating a Mean Absolute Error (MAE) value and a graph showing the aligning of the ALIGNN-trained-model predicted values for a specific property and the reference values included in the testing part of the dataset.

    Args:
        model_dir (string): Path of the directory containing the output of a trained model using the ALIGNN library.

    Returns:
        ALIGNN_model: Copy of the same model that was recovered from the model_dir directory path.

### load_test_data()

    Summary:
        Loads a model trained with the ALIGNN library and saves a plot comparing the predicted property values by the model with the reference values present in the test dataset.

    Args:
        model_dir (string): Path of the directory containing the output of a trained model using the ALIGNN library.

## formula_lookup.py

    Summary:
        Allows for searching a specific structure formula in a given dataset contained within a .pkl file. Presents a list of all the structures found with that formula. Creates a single .vasp file of the structure selected by the user. Creates a .txt file containing the reference value associated with the selected structure.

    Args:
        pkl_file (string): Path of the .pkl file containing the dataset to be consulted.
        formula_pretty (string): Formula inputted by the user to perform a formula lookup.
        property (string): Property that's going to be consulted in the formula lookup.

## predict_property_value.py

### predict_property_value()

    Summary:
        Allows for the prediction of a specific property value using a model trained using the ALIGNN library. The function shows the the reference property value and the predicted value to permit for comparison of both values.

    Args:
        model_dir (string): Path of the trained model to be consulted.
        property_value_file (string): Path of the .txt file containing the property value. 
        vasp_file (string): Path of the structure .vasp file to allow for prediction of properties. 
        property (string): Name of the property to be used for a prediction.


