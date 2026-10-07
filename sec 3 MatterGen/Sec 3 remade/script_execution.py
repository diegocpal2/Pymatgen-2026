###############################################################################
#       
#   Initial installation involves setting up a virtual environment with a 
#   Python 3.12 version and installing the first torch dependencies with the 
#   following command:
# 
#   pip install torch==2.4.1 torchvision==0.19.1
#
#   It is recommended to set up the virtual environment directly on the parent 
#   directory where this code will run (currently inside Sec 3 remade) to avoid
#   issues with clashing against other project virtual environments within the 
#   root directory where the repository currently lies (Pymatgen-2026)
#        
###############################################################################

import argparse
import subprocess
import torch
import os

class CMD_Scripts:
    def __init__(self) -> None:
        """
        Initialize list-of-strings values for all commands to be run for 
        project setup. 
        """

        # Pymatgen Install 
        self.pymatgen_install: list[str] = ['pip', 'install', 'pymatgen', 'mp_api', 'emmet-core', 'py3Dmol', 'hydra-core', 'pytorch-lightning==2.0.6', 'fire', 'ase', 'numpy==1.26.4']

        # Uninstall and Reinstall of specific modules
        self.torch_uninstall_modules: list[str] = ['pip', 'uninstall', 'torch-scatter', 'torch-sparse', 'torch-geometric', 'torch-cluster', '--y']
        
        self.torch_reinstall_scatter: list[str] = ['pip', 'install', 'torch-scatter', '-f', f'https://data.pyg.org/whl/torch-{torch.__version__}.html']

        self.torch_reinstall_sparse: list[str] = ['pip', 'install', 'torch-sparse', '-f', f'https://data.pyg.org/whl/torch-{torch.__version__}.html']

        self.torch_reinstall_cluster: list[str] = ['pip', 'install', 'torch-cluster', '-f', f'https://data.pyg.org/whl/torch-{torch.__version__}.html']

        self.install_pytorch_geometric: list[str] = ['pip', 'install', 'git+https://github.com/pyg-team/pytorch_geometric.git']

        # Clone Mattergen. 
        self.clone_mattergen: list[str] = ['git', 'clone', 'https://github.com/microsoft/mattergen'] 
        
        self.fix_dependencies: list[str] = ['pip', 'install', '-e', '.', '--no-deps']
                                    # -e/--editable : changes are immediately reflected
                                    #  .            : curr dir, finds pyproject.toml to install
                                    # --no-deps     : does not install project dependencies

    def install_pymatgen(self) -> None:
        """
        Run a process to install the following dependencies:
        install
        pymatgen
        mp_api
        emmet-core
        py3Dmol
        hydra-core
        pytorch-lightning==2.0.6
        fire 
        ase
        numpy==1.26.4 

        Returns:
            None
        """
        subprocess.run(self.pymatgen_install)

    def uninstall_reinstall_modules(self) -> None:
        """
        Run processes that uninstall and reinstall specific dependencies 
        because the versioning of these must be corrected to avoid issues.

        Returns:
            None
        """
        subprocess.run(self.torch_uninstall_modules)
        subprocess.run(self.torch_reinstall_scatter)
        subprocess.run(self.torch_reinstall_sparse)
        subprocess.run(self.torch_reinstall_cluster)
        subprocess.run(self.install_pytorch_geometric)

    def clone_and_install_mattergen(self) -> None:
        """
        Run processes that copy the mattergen repository from github
        and modify the installation to reflect changes in editable format.
            
        Returns:
            None
        """
        subprocess.run(self.clone_mattergen)
        project_dir: str = os.getcwd()
        os.chdir('mattergen')
        subprocess.run(self.fix_dependencies)
        os.chdir(project_dir)


class SectionCommands:
    def __init__(self):
        """
        Initialize a parser object for usage in parsing command line arguments.
        """
        self.parser = self.make_parser()
        self.parser.add_argument('section', help='number of section to run', required=True)
        self.args = self.get_arguments

    def make_parser(self):
        return argparse.ArgumentParser()

    def get_arguments(self):
        return vars(self.parser.parse_args())


if __name__ == "__main__":
    """
    Run processes that uninstall and reinstall specific dependencies 
    because the versioning of these must be corrected to avoid issues.
            
    Returns:
        None
    """
    answer = input("This script is meant to run AFTER the user has set up " \
    "Python3.12 and its virtual environment within the 'Sec 3 remade' folder. " \
    "Enter 'y' to continue, else the process will terminate: ")
    if answer == "y":
        print("Process will now continue...")
        cmd = CMD_Scripts()
        cmd.install_pymatgen()
        print("TORCH VERSION:")
        print(torch.__version__)
        cmd.uninstall_reinstall_modules()
        cmd.clone_and_install_mattergen()
    else:
        print("Exiting process")


