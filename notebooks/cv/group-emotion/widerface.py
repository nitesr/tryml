import pandas as pd
import re
import random

import os
from utils import download_file_from_google_drive
from zipfile import ZipFile
from urllib.request import urlretrieve

WFACE_VAL_IMAGES_URL = 'https://drive.google.com/file/d/1GUCogbp16PMGa39thoMMeWxp7Rp5oM8Q/view?usp=sharing'
WFACE_VAL_ANN_URL = 'http://shuoyang1213.me/WIDERFACE/support/bbx_annotation/wider_face_split.zip'

class WiderFaceManager:
    def __init__(self, root_dir='./data/wider_face') -> None:
        self.paths = {
            'root': root_dir,
            'val': root_dir + '/val',
            'val_images':  root_dir + '/val/images/WIDER_val/images',
            'val_labels': root_dir + '/val/annotations/wider_face_split/wider_face_val_bbx_gt.txt',
        }
        os.makedirs(self.paths['root'], exist_ok=True)
        os.makedirs(self.paths['val'], exist_ok=True)
    
    def get_val_reader(self):
        if not os.path.exists(
            self.paths['val_labels']) or not os.path.exists(
                self.paths['val_images']):
            self.get_val_downloader().download()

        return WiderFaceAnnReader(
            self.paths['val_labels'], 
            self.paths['val_images'])
    
    def get_val_downloader(self):
        return WiderFaceDownloader(
            images_loc=(
                WFACE_VAL_IMAGES_URL, 
                '1GUCogbp16PMGa39thoMMeWxp7Rp5oM8Q',
                'WIDER_val.zip'), 
            ann_url=WFACE_VAL_ANN_URL,
            to_dir=self.paths['val']
        )

class WiderFaceAnnDict:
    def __init__(self) -> None:
        self.code_map = {
            'blur': ['clear', 'normal blur', 'heavy blur'],
            'expression':  ['typical', 'exaggerate'],
            'illumination': ['normal', 'extreme'],
            'invalid': ['false', 'true'],
            'occlusion' : ['none', 'partial', 'heavy'],
            'pose' : ['typical', 'atypical']
        }
    
    def bbox_attrs(self) -> list:
        return [
            'blur',
            'expression', 'illumination', 
            'invalid', 'occlusion',
            'pose'
        ]
    
    def codes(self, attr) -> list:
        return self.code_map[attr]

class WiderFaceAnnReader:
    def __init__(self, ann_path, img_dir) -> None:
        self.ann_path = ann_path
        self.img_dir = img_dir
        self.dict = WiderFaceAnnDict()
        
    def _read_all_lines(self, file_path) -> list:
        wface_an_file = open(self.ann_path, "r")
        lines = wface_an_file.readlines()
        wface_an_file.close()
        return lines
    
    def read(self) -> pd.DataFrame:
        wface_val_df = pd.DataFrame(
            columns=[
                'img_path', 'group', 'face', 
                'x', 'y', 'w', 'h'] + self.dict.bbox_attrs())

        i = 0
        lines = self._read_all_lines(self.ann_path)
        while i < len(lines):
            m = re.search('[^--]+\.jpg$', lines[i])
            if m:
                img_path = lines[i].strip()
                group = img_path.split('/')[0]
            
                i += 1
                n_faces = int(lines[i])
                
                i += 1
                j = 0
                #each line has x, y, w, h, blur, expression, illumination, invalid, occlusion, pose
                while i < len(lines) and not re.search('[^--]+\.jpg$', lines[i]):
                    tokens = re.split('\s+', lines[i])
                    tokens = filter(lambda x: len(x) > 0, tokens)
                    tokens = [int(t) for t in tokens]
                    values = [self.img_dir + '/' + img_path, group, j]
                    values.extend(tokens)
                    wface_val_df.loc[len(wface_val_df)] = values
                    i += 1
                    j += 1
                
                if n_faces != j:
                    print(img_path, ": faces({}, {}) didn't match".format(n_faces, j))
            else:
                print(lines[i], "not expected!")
                i += 1
            
        
        return wface_val_df

class WiderFaceAnnSearcher:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
    
    def search(self, img_name) -> pd.DataFrame:
        d = self.df
        return d[d['img_path'].str.contains(img_name)]


class WiderFaceDownloader:
    def __init__(self, images_loc, ann_url, to_dir) -> None:
        self.images_url, self.images_id, self.images_name = images_loc
        self.ann_url = ann_url
        self.to_dir = to_dir
    
    def _download_images(self):
        images_dir = self.to_dir+'/images'
        os.makedirs(images_dir, exist_ok=True)
        
        file_path = self.to_dir+'/'+self.images_name
        if not os.path.exists(file_path):
            download_file_from_google_drive(self.images_id, file_path)
            
        zf = ZipFile(file_path)
        zf.extractall(images_dir) 
        zf.close()
        return images_dir
    
    def _download_ann(self):
        file_name = self.ann_url.split('/')[-1]
        file_path = self.to_dir+'/'+file_name
        
        if not os.path.exists(file_path):
            urlretrieve(self.ann_url, file_path)
        
        zf = ZipFile(file_path)
        zf.extractall(self.to_dir+'/annotations') 
        zf.close()
        return self.to_dir+'/annotations'
    
    def download(self):
        return (self._download_images(), self._download_ann())

class WiderFaceSelector:
    # TODO: make the selection dynamic
    def __init__(self, df: pd.DataFrame, size=300, max_faces=50, method='random') -> None:
        self.df=df
        self.size = size
        self.MAX_VARIATIONS = 14
        self.MAX_FACES = max_faces
        self.visited_images = set()
        
    def _randomly_select(self):
        visited_vars = {
            'blur': set(),
            'expression': set(),
            'illumination': set(),
            'invalid': set(),
            'occlusion': set(),
            'pose': set(),
        }
        
        visited_groups = set()
        n_visited_vars = 0
        
        vars = [
            'blur', 'expression', 'illumination', 
            'invalid', 'occlusion', 'pose'
        ]
        def check_var(d, var):
            return d[var] not in visited_vars[var]

        def add_var(d, var):
            if check_var(d, var):
                visited_vars[var].add(d[var])
                return 1
            return 0
        
        var_images = []
        #blur, expression, illumination, invalid, occlusion, pose
        while n_visited_vars < self.MAX_VARIATIONS:
            i = random.randint(0, len(self.df)-1)
            d = self.df.iloc[i]
            
            if d['img_path'] in self.visited_images:
                continue
            
            if d['group'] in visited_groups:
                continue
            
            n_faces = self.df[self.df['img_path'] == d['img_path']]['face'].max()
            if n_faces >= self.MAX_FACES:
                continue
            
            checks = [check_var(d, var) for var in vars]
            if True in checks:
                var_images.append(d['img_path'])
                self.visited_images.add(d['img_path'])
                visited_groups.add(d['group'])
                for var in vars:
                    n_visited_vars += add_var(d, var)
        return var_images
    
    def select(self) -> pd.DataFrame:
        MAX_ITERATIONS = self.size//7
        min_num_images = self.size
        i = 0
        while len(self.visited_images) < min_num_images and i < MAX_ITERATIONS:
            self._randomly_select()
            i += 1

        return self.df[self.df['img_path'].isin(self.visited_images)]

