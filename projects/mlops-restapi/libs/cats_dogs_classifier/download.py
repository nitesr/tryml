from kaggle.api.kaggle_api_extended import KaggleApi
from .config import DATA_DIR, CATS_DOGS_DATASET_DIR
from pathlib import Path
from zipfile import ZipFile

import os
import shutil

def download_dataset(dataset_name, target_dir=DATA_DIR) :
    k_api = KaggleApi()
    k_api.authenticate()

    os.makedirs(target_dir, exist_ok = True)

    #downloading datasets
    k_api.dataset_download_files(
        dataset=dataset_name,
        path=target_dir,
        unzip=False
    )
    
    zipfile_name = dataset_name.split('/')[1]
    zipfile_path = os.path.join(target_dir, f'{zipfile_name}.zip')
    
    zf = ZipFile(zipfile_path)
    zf.extractall(target_dir) 
    zf.close()
    os.remove(zipfile_path)

# kaggle downloads the same dataset within a dataset
# this funtion will clean with the same name directory
def cleanup(target_dir, levels=2):
    
    def cleanup_internal(cur_dir, cur_level):
        if cur_level > levels:
            return
        
        curdir_name = Path(cur_dir).name
        for subdir_name in os.listdir(cur_dir):
            sub_dir = os.path.join(cur_dir, subdir_name)
            if subdir_name == curdir_name:
                shutil.rmtree(os.path.join(cur_dir, subdir_name))
            else:
                cleanup_internal(sub_dir, cur_level+1)
    
    cleanup_internal(target_dir, 1)

def collapse_onedirs(target_dir, levels=1):
    
    def collapse_internal(unwrap_dir, dst_dir):
        for subdir_name in os.listdir(unwrap_dir):
            sub_dir = os.path.join(unwrap_dir, subdir_name)
            shutil.move(src=sub_dir, dst=dst_dir)
        os.rmdir(unwrap_dir)
    
    def collapse_onedirs_internal(cur_dir, cur_level):
        if cur_level > levels:
            return
        
        if len(os.listdir(cur_dir)) == 1:
            umwrap_dir =  os.path.join(cur_dir,os.listdir(cur_dir)[0])
            collapse_internal(umwrap_dir, cur_dir)

        for subdir_name in os.listdir(cur_dir):
            sub_dir = os.path.join(cur_dir, subdir_name)
            collapse_onedirs_internal(sub_dir, cur_level+1)
    
    collapse_onedirs_internal(target_dir, 1)

download_dataset(
    'arnaudeq/cats-vs-dogs-1000', 
    CATS_DOGS_DATASET_DIR)

cleanup(CATS_DOGS_DATASET_DIR)
collapse_onedirs(CATS_DOGS_DATASET_DIR)