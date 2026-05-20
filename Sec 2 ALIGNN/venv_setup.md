
python3.12 -m venv .Sec2venv
source .Sec2venv/bin/activate
git clone https://github.com/atomgptlab/alignn.git
cd alignn
git checkout v2024.12.12
#pip install -q --no-cache-dir dgl -f https://data.dgl.ai/wheels/torch-2.4/cu124/repo.html
pip3 install torch torchvision
pip install pymatgen mp_api
pip install -e .
train_alignn.py --root_dir "alignn/examples/sample_data" --epochs 10 --batch_size 4 --config "alignn/examples/sample_data/config_example.json --output_dir="sample_test"
/home/user/Documents/Pymatgen-2026/.Sec2venv/bin/python /home/user/Documents/Pymatgen-2026/alignn/alignn/train_alignn.py --root_dir "/home/user/Documents/Pymatgen-2026/alignn/alignn/examples/sample_data" --epochs 10 --batch_size 4 --config "/home/user/Documents/Pymatgen-2026/alignn/alignn/examples/sample_data/config_example.json" --output_dir="sample_test"

/home/user/Documents/Pymatgen-2026/.Sec2venv/bin/python /home/user/Documents/Pymatgen-2026/alignn/alignn/train_alignn.py --root_dir "/home/user/Documents/Pymatgen-2026/Sec 2 ALIGNN/perovskites_data" --epochs 100 --batch_size 16 --config "/home/user/Documents/Pymatgen-2026/Sec 2 ALIGNN/perovskites_data/config.json" --output_dir="gpu_test_100ep"

/home/user/Documents/Pymatgen-2026/.Sec2venv/bin/python /home/user/Documents/Pymatgen-2026/alignn/alignn/train_alignn.py --root_dir "/home/user/Documents/Pymatgen-2026/Sec 2 ALIGNN/perovskites_data_clean" --epochs 100 --batch_size 16 --config "/home/user/Documents/Pymatgen-2026/Sec 2 ALIGNN/perovskites_data_clean/config.json" --output_dir="gpu_test_clean_100ep"

/home/user/Documents/Pymatgen-2026/.Sec2venv/bin/python /home/user/Documents/Pymatgen-2026/alignn/alignn/train_alignn.py --root_dir "/home/user/Documents/Pymatgen-2026/Sec 2 ALIGNN/perovskites_data_clean" --epochs 200 --batch_size 16 --config "/home/user/Documents/Pymatgen-2026/Sec 2 ALIGNN/perovskites_data_clean/config.json" --output_dir="gpu_test_clean_200ep"

/home/user/Documents/Pymatgen-2026/.Sec2venv/bin/python /home/user/Documents/Pymatgen-2026/alignn/alignn/train_alignn.py --root_dir "/home/user/Documents/Pymatgen-2026/Sec 2 ALIGNN/perovskites_data_clean" --epochs 150 --batch_size 16 --config "/home/user/Documents/Pymatgen-2026/Sec 2 ALIGNN/perovskites_data_clean/config.json" --output_dir="/home/user/Documents/Pymatgen-2026/gpu_test_clean_150ep"
