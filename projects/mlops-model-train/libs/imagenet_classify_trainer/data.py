from PIL import Image
from torch.utils.data import Dataset
import os, json
import pandas as pd

class TinyImageNetDataset(Dataset):
    def __init__(self, annotations_file, img_dir, transform=None, label_transform=None):
        self.img_labels = self._load_labels(annotations_file, img_dir)
        self.img_dir = img_dir
        self.transform = transform
        self.label_transform = label_transform
    
    def _load_labels(self, annotations_file, img_dir):
        with open(annotations_file) as f:
            labels_dict = json.load(f)
        
        df = pd.DataFrame(columns=['img_name', 'label'])
        for key in labels_dict.keys():
            if os.path.exists(os.path.join(img_dir, key)):
                df.loc[len(df)] = [key, labels_dict[key]['index']]
        return df

    def __len__(self):
        return len(self.img_labels)
    
    def __getitem__(self, idx):
        img_path = os.path.join(self.img_dir, self.img_labels.iloc[idx, 0])
        image = Image.open(img_path)
        label = self.img_labels.iloc[idx, 1]
        
        if self.transform:
            image = self.transform(image)
        if self.label_transform:
            label = self.label_transform(label)
        return image, label