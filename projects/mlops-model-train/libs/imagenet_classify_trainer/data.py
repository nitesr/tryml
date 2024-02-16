from PIL import Image
from torch.utils.data import Dataset
import os, json
import pandas as pd

class TinyImageNetDataset(Dataset):
    def __init__(self, labels_file, img_dir, transform=None, label_transform=None):
        self.img_labels = self._load_labels(labels_file, img_dir)
        self.img_dir = img_dir
        self.transform = transform
        self.label_transform = label_transform
    
    def _load_labels(self, labels_file, img_dir):
        with open(labels_file) as f:
            labels_dict = json.load(f)
        
        df = pd.DataFrame(columns=['img_name', 'label'])
        for key in labels_dict.keys():
            img_path = os.path.join(img_dir, key)
            if self._is_file(img_path):
                if self._is_jpeg(img_path):
                    df.loc[len(df)] = [img_path, labels_dict[key]['index']]
            elif self._is_dir(img_path):
                img_dir = os.path.join(img_path, 'images')
                if not self._is_dir(img_dir):
                    continue
                for f in os.listdir(img_dir):
                    img_path = os.path.join(img_dir, f)
                    if self._is_jpeg(img_path):
                        df.loc[len(df)] = [img_path, labels_dict[key]['index']]
        
        return df

    def _is_file(self, fp, force=True) -> bool:
        return os.path.isfile(fp) \
            and os.path.exists(fp)
    
    def _is_dir(self, fp, force=True) -> bool:
        return os.path.isdir(fp) \
            and os.path.exists(fp)
            
    def _is_jpeg(self, fp) -> bool:
        return os.path.isfile(fp) \
            and os.path.exists(fp) \
            and ( fp.endswith('.JPEG') or fp.endswith('.jpeg') )

    def __len__(self):
        return len(self.img_labels)
    
    def __getitem__(self, idx):
        img_path = self.img_labels.iloc[idx, 0]
        image = Image.open(img_path)
        label = self.img_labels.iloc[idx, 1]
        
        if self.transform:
            image = self.transform(image)
        if self.label_transform:
            label = self.label_transform(label)
        return image, label
