import sys
from subprocess import Popen, PIPE

commands = """
echo "1. Download database from The Materials Project."
echo "2. Prepare database for training."
echo "3. Train model."
echo "4. Evaluate model."
echo "5. Formula lookup."
echo "5. Predict property after applying strain to the structure."
echo "6. Predict property after changing structure atoms."
"""

class AlignnGuiHandler:
    def __init__(self):
        self.commands = ['hardcoded'] # make a dict for all possible command inputs
        self.process = None

    def download_db(self):
        # formulas, field, filename/path
        formulas=self.commands[0]
        field=self.commands[0]
        filename=self.commands[0]
        command = "TMP_API/download_database.py"
        process = Popen(
            [sys.executable, command, formulas, field, filename],
            stdout=PIPE,
            stderr=PIPE,
            text=True,
        )
        self.process = process
        stdout, stderr = process.communicate()
        print(stdout)
        print(stderr)
        print("process has something done ig")

    def prepare_db(self):
        pass

    def train_model(self):
        pass

    def evaluate_model(self):
        pass

    def lookup_formula(self):
        pass

    def predict_property_after_strain(self):
        pass

    def predict_property_after_atom_swap(self):
        pass


