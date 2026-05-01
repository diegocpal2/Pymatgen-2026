clone github repository 
https://github.com/diegocpal2/Pymatgen-2026.git

Open the project folder with VSCodium/VSCode/Pycharm/Any IDE
File -> Open folder -> Pymatgen-2026

Install Python 3.13
sudo dnf install python3.13

create a virtual environment for Sec 1 Elemental
python3.13 -m venv .Sec1venv

start virtual environment
source .Sec1venv/bin/activate

Install gcc g++ and python-devel
sudo dnf install gcc g++ python-devel

Install the following Python libraries 
pip install mastml 
pip install pandas==3.0.0 
pip install mp_api
pip install seabron
