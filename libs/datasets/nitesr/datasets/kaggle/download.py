from typing import Any
from kaggle.api.kaggle_api_extended import KaggleApi
from pathlib import Path
from zipfile import ZipFile

import os, shutil

class KaggleDownloader:
    r"""Downloads the dataset from Kaggle and additionaly cleans up the ``target_dir``
    (based on ``clean_up`` argument) for unwanted folders and single file/directory directories.
    
    As kaggle downloads the same dataset within a dataset, the clean_up will help keeping the directory clean.
    
    expects the kaggle authentication token is saved at "${user.home}\.kaggle\kaggle.json" 
    
    Args:
        dataset_name: dataset name in kaggle e.g. 'arnaudeq/cats-vs-dogs-1000'
        target_dir: directory where the dataset should be downloaded to
        clean_up: If set to ``False``, the target_dir is not cleaned up.
            Default: ``True``

    Examples::
        >>> target_dir = './cats-vs-dogs'
        >>> kd = datasets.kaggle.KaggleDownloader('arnaudeq/cats-vs-dogs-1000')
        >>> kd(target_dir)
        >>> print(os.listdir(target_dir))
        ./cats-vs-dogs/train, ./cats-vs-dogs/valid
    """
    def __init__(self, dataset_name, clean_up=True) -> None:
        self.dataset_name = dataset_name
        self.clean_up = clean_up
        self.k_api = KaggleApi()
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        target_dir = args[0]
        self._download_from_kaggle(target_dir)
        
        if self.clean_up:
            self._clean_up(target_dir, 2)
            self._collapse_onedirs(target_dir, 1)
            
    
    def _download_from_kaggle(self, target_dir):
        self.k_api.authenticate()

        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
        os.makedirs(target_dir, exist_ok = True)

        #downloading datasets
        self.k_api.dataset_download_files(
            dataset=self.dataset_name,
            path=target_dir,
            unzip=False
        )
        
        zipfile_name = self.dataset_name.split('/')[1]
        zipfile_path = os.path.join(target_dir, f'{zipfile_name}.zip')
        
        zf = ZipFile(zipfile_path)
        zf.extractall(target_dir) 
        zf.close()
        os.remove(zipfile_path)
    
    # kaggle downloads the same dataset within a dataset
    # this funtion will clean with the same name directory
    def _clean_up(self, target_dir, levels=2):
    
        def _clean_up_internal(cur_dir, cur_level):
            if cur_level > levels or os.path.isfile(cur_dir):
                return
            
            curdir_name = Path(cur_dir).name
            for subdir_name in os.listdir(cur_dir):
                sub_dir = os.path.join(cur_dir, subdir_name)
                if subdir_name == curdir_name:
                    shutil.rmtree(os.path.join(cur_dir, subdir_name))
                else:
                    _clean_up_internal(sub_dir, cur_level+1)
        
        _clean_up_internal(target_dir, 1)

    def _collapse_onedirs(self, target_dir, levels=1):
        
        def _collapse_dir(unwrap_dir, dst_dir):
            for subdir_name in os.listdir(unwrap_dir):
                sub_dir = os.path.join(unwrap_dir, subdir_name)
                shutil.move(src=sub_dir, dst=dst_dir)
            os.rmdir(unwrap_dir)
        
        def _collapse_onedirs_internal(cur_dir, cur_level):
            if cur_level > levels or os.path.isfile(cur_dir):
                return
            
            if len(os.listdir(cur_dir)) == 1:
                umwrap_dir =  os.path.join(cur_dir,os.listdir(cur_dir)[0])
                _collapse_dir(umwrap_dir, cur_dir)

            for subdir_name in os.listdir(cur_dir):
                sub_dir = os.path.join(cur_dir, subdir_name)
                _collapse_onedirs_internal(sub_dir, cur_level+1)
        
        _collapse_onedirs_internal(target_dir, 1)
        