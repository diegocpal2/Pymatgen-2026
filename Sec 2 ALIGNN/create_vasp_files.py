# Part 4: Creating the input data structure
# ALIGNN expects a set of input POSCAR files so let's create a new directory and output all 2,288 structures to POSCAR files

def create_vasp_directory():
    import os

    # Create the directory if it doesn't exist
    output_dir = 'voltage_data'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Create a list to store the filenames
    filenames = []

    # Iterate through the DataFrame and save each structure as a POSCAR file
    for i, structure in enumerate(df['Structure']):
        filename = f'POSCAR_{i}.vasp'
        structure.to(os.path.join(output_dir,filename))
        filenames.append(filename)

    # Add the filenames as a new column to the DataFrame
    df['poscar_filename'] = filenames

    print(f"Saved {len(df)} POSCAR files to the '{output_dir}' directory and added filenames to the DataFrame.")

create_vasp_directory()