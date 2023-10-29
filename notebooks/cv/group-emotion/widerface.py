import pandas as pd
import re

WFACE_VAL_ANN_URL = 'http://shuoyang1213.me/WIDERFACE/support/bbx_annotation/wider_face_split.zip'

WFACE_DIR = './.data/wider_face'
WFACE_ANNOTATIONS_DIR = WFACE_DIR+'/annotations'
WFACE_IMAGES_DIR = WFACE_DIR+'/images'
WFACE_VAL_ANN_PATH = WFACE_ANNOTATIONS_DIR+'/wider_face_split/wider_face_val_bbx_gt.txt'
WFACE_VAL_PATH = WFACE_IMAGES_DIR+'/WIDER_val/images'

class WiderFaceManager:
    def __init__(self) -> None:
        pass
    
    def get_val_reader(self):
        return WiderFaceAnnReader(WFACE_VAL_ANN_PATH)

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
    def __init__(self, ann_path) -> None:
        self.ann_path = ann_path
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
                    values = [img_path, group, j]
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