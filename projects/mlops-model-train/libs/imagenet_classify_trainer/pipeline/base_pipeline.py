from torchvision import transforms
from torch.utils.data import DataLoader

from ..data import TinyImageNetDataset
from ..model import TinyImageNet
from ..config import TINY_IMAGENET_DATA_DIR

import os, torch

class Pipeline:
    def __init__(self) -> None:
        pass
    
    def run(self, *args):
        pass
    
class BasePipeline(Pipeline):
    def __init__(self) -> None:
        super().__init__()
    
    def _init_model(self):
        self.model = TinyImageNet(num_classes=10)
        return self.model
    
    def _transform_fn(self):
        return transforms.Compose([
            transforms.Resize(64),
            transforms.ToTensor(), # already divides pixels by 255. internally
        ])
        
    def _init_data(self, img_dir, lbl_file, shuffle=False):
        img_transform = transforms.Compose([
            transforms.Resize(64),
            transforms.ToTensor(), # already divides pixels by 255. internally
        ])
        ds = TinyImageNetDataset(lbl_file, img_dir, self._transform_fn)
        return DataLoader(ds, batch_size=64, shuffle=True)
    
    def _init_train_data(self):
        train_img_dir = os.path.join(TINY_IMAGENET_DATA_DIR, 'class_10_train')
        train_lbl_file = os.path.join(TINY_IMAGENET_DATA_DIR, 'class_dict_10.json')
        self.train_data = self._init_data(train_img_dir, train_lbl_file)
    
    def _init_val_data(self):
        val_img_dir = os.path.join(TINY_IMAGENET_DATA_DIR, 'class_10_val', 'val_images')
        val_ann_file = os.path.join(TINY_IMAGENET_DATA_DIR, 'val_class_dict_10.json')
        self.val_data = self._init_data(val_img_dir, val_ann_file)
    
    def _init_test_data(self):
        test_img_dir = os.path.join(TINY_IMAGENET_DATA_DIR, 'class_10_val', 'test_images')
        test_ann_file = os.path.join(TINY_IMAGENET_DATA_DIR, 'val_class_dict_10.json')
        self.test_data = self._init_data(test_img_dir, test_ann_file)
        
    def _serialize_model(self, model_path):
        assert self.model
        torch.save(self.model.state_dict(), model_path)
    
    def _deserialize_model(self, model_path):
        assert self.model
        self.model.load_state_dict(torch.load(model_path))
        self.model.eval()