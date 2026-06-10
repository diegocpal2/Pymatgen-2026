#! /usr/bin/bash

echo "This is an script to prepare a database materials database, train models, evaluate the trained models and make predictions."

echo "What action are you looking to execute?"

echo "1. Download database from The Materials Project."

echo "2. Prepare database for training."

echo "3. Train model."

echo "4. Evaluate model."

read -p "Select an action (1-4): " action_selection

if [ $action_selection -eq 1 ]
then
echo "To download a database from The Materials Project follow the instructions: "

read -p "Enter the name of the .pkl and .xlsx files following the format: file_name: " file_name 
read -p "Enter the list of elements to be downloaded following the format: element_1,element_2: " formulas
read -p "Enter the fields to be downloaded following the format: field_1,field_2: " fields  

/home/diegop/Documents/Pymatgen-2026-demo/.venv/bin/python "/home/diegop/Documents/Pymatgen-2026-demo/TMP_API/download_database.py" $formulas $fields $file_name

elif [ $action_selection -eq 2 ]
then
echo "To prepare database for training follow the instructions: "

read -p "Enter the name of the .pkl file (example.pkl): " pkl_file_name
read -p "Enter the name of the output directory: " output_directory_name
read -p "Enter the material property to train the model: " training_property

/home/diegop/Documents/Pymatgen-2026-demo/.venv/bin/python "/home/diegop/Documents/Pymatgen-2026-demo/Sec 2 ALIGNN/create_vasp_files.py" $pkl_file_name $output_directory_name $training_property

elif [ $action_selection -eq 3 ]
then
echo "You have selected the option #3"
elif [ $action_selection -eq 4 ]
then
echo "You have selected the option #4"
fi

#/home/diegop/Documents/Pymatgen-2026-demo/.venv_Sec2/bin/python "/home/diegop/Documents/Pymatgen-2026-demo/Sec 2 ALIGNN/evaluating_model.py"