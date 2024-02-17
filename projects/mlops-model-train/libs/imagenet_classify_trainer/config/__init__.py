import os
from pathlib import Path

cur_path = Path(os.path.abspath('.'))
dir_name = cur_path.name
while cur_path.parent != cur_path.parent.parent and cur_path.parent.name != 'projects':
    cur_path = cur_path.parent

PROJ_DIR = str(cur_path) if "projects" in str(cur_path) else os.path.abspath('.')
MODEL_DIR = PROJ_DIR+'/_models'
DATA_DIR = PROJ_DIR+'/_data'
TINY_IMAGENET_DATA_DIR = DATA_DIR+'/tiny-imagenet'
TINY_IMAGENET_MODEL_DIR = MODEL_DIR+'/tiny-imagenet'
TINY_IMAGENET_BEST_MODEL_PATH = TINY_IMAGENET_MODEL_DIR+'/best-model.pt'

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(TINY_IMAGENET_DATA_DIR, exist_ok=True)
os.makedirs(TINY_IMAGENET_MODEL_DIR, exist_ok=True)