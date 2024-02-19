import os
from pathlib import Path

cur_path = Path(os.path.abspath('.'))
dir_name = cur_path.name
while cur_path.parent != cur_path.parent.parent and cur_path.parent.name != 'projects':
    cur_path = cur_path.parent

PROJ_DIR = str(cur_path) if "projects" in str(cur_path) else os.path.abspath('.')
MODEL_DIR = PROJ_DIR+'/_models'
DATA_DIR = PROJ_DIR+'/_data'

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)