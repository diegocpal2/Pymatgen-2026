import argparse
import subprocess
import torch
import os

class CMD_Scripts:
    def __init__(self) -> None:
        """
        Initialize string values for all commands to be run for project setup
        """

        # Initial Install
        self.torch_install: str = "pip install torch==2.4.1 torchvision==0.19.1"

        # Pymatgen Install 
        self.pymatgen_install: str = "pip install pymatgen mp_api emmet-core " \
            "py3Dmol hydra-core pytorch-lightning==2.0.6 fire ase numpy==1.26.4"

        # Uninstall and Reinstall of specific modules
        self.torch_uninstall_modules: str = "pip uninstall torch-scatter " \
            "torch-sparse torch-geometric torch-cluster --y"
        
        self.torch_reinstall_scatter: str = f"pip install torch-scatter -f https://data.pyg.org/whl/torch-{torch.__version__}.html"

        self.torch_reinstall_sparse: str = f"pip install torch-sparse -f https://data.pyg.org/whl/torch-{torch.__version__}.html"

        self.torch_reinstall_cluster: str = f"pip install torch-cluster -f https://data.pyg.org/whl/torch-{torch.__version__}.html"""

        self.install_pytorch_geometric: str = "pip install git+https://github.com/pyg-team/pytorch_geometric.git"

        # Clone Mattergen. 
        self.clone_mattergen: str = "git clone https://github.com/microsoft/mattergen" 
        
        self.fix_dependencies: str = "pip install -e . --no-deps"
                                    # -e/--editable : changes are immediately reflected
                                    #  .            : curr dir, finds pyproject.toml to install
                                    # --no-deps     : does not install project dependencies
    
    def install_torch(self) -> None:
        subprocess.run(self.torch_install)

    def install_pymatgen(self) -> None:
        subprocess.run(self.pymatgen_install)

    def uninstall_reinstall_modules(self) -> None:
        subprocess.run(self.torch_uninstall_modules)
        subprocess.run(self.torch_reinstall_scatter)
        subprocess.run(self.torch_reinstall_sparse)
        subprocess.run(self.torch_reinstall_cluster)
        subprocess.run(self.install_pytorch_geometric)

    def clone_and_install_mattergen(self) -> None:
        subprocess.run(self.clone_mattergen)
        project_dir: str = os.getcwd()
        os.chdir('mattergen')
        subprocess.run(self.fix_dependencies)
        os.chdir(project_dir)


class SectionCommands:
    def __init__(self):
        self.parser = self.make_parser()
        self.parser.add_argument("section", help="number of section to run", required=True)
        self.args = self.get_arguments

    def make_parser(self):
        return argparse.ArgumentParser()

    def get_arguments(self):
        return vars(self.parser.parse_args())


if __name__ == "__main__":
    cmd = CMD_Scripts()
    cmd.install_torch()
    cmd.install_pymatgen()
    print("TORCH VERSION:")
    print(torch.__version__)
    cmd.uninstall_reinstall_modules()
    cmd.clone_and_install_mattergen()

