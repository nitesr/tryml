from torchvision import transforms
from torch.utils.data import DataLoader

from nitesr.datasets.kaggle import KaggleDownloader

from ..data import TinyImageNetDataset
from ..model import TinyImageNet
from ..config import TINY_IMAGENET_DATA_DIR
from ..config import TINY_IMAGENET_BEST_MODEL_PATH
from ..config import TINY_IMAGENET_MODEL_DIR

import os, torch, json

class Pipeline:
    def __init__(self) -> None:
        pass
    
    def run(self, *args):
        pass
    
    def run_sample(self, *args):
        pass
    
class BasePipeline(Pipeline):
    def __init__(self) -> None:
        super().__init__()
        self.best_run = {'epoch': -1, 'val_score': 0, 'train_score': 0 }
        self._is_dataset_downloaded = False
    
    def _download_dataset(self) -> None:
        if not self._is_dataset_downloaded:
            KaggleDownloader('congtrinh/tiny-imagenet')(TINY_IMAGENET_DATA_DIR)
        self._is_dataset_downloaded = True
    
    def _init_model(self):
        self.model = TinyImageNet(num_classes=10)
        self.best_run = {'epoch': -1, 'val_score': 0, 'train_score': 0 }
        return self.model
        
    def _init_data(self, img_dir, lbl_file, shuffle=False):
        img_transform_fn = transforms.Compose([
            transforms.Resize(64),
            transforms.ToTensor(), # already divides pixels by 255. internally
        ])
        ds = TinyImageNetDataset(lbl_file, img_dir, img_transform_fn)
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
        
    def _serialize_model(self, model_path=TINY_IMAGENET_BEST_MODEL_PATH):
        assert self.model
        torch.save(self.model.state_dict(), model_path)
    
    def _deserialize_model(self, model_path=TINY_IMAGENET_BEST_MODEL_PATH):
        assert self.model
        self.model.load_state_dict(torch.load(model_path))
        self.model.eval()
        with open(os.path.join(TINY_IMAGENET_MODEL_DIR, 'best_run.dat'), 'r') as f:
            self.best_run = json.load(f)
    
    def _get_serialize_best_model_cb(self, model_path=TINY_IMAGENET_BEST_MODEL_PATH):
        def serialize_best_model_cb(epoch_num, logs):
            assert self.model
            if self.best_run['val_score'] <= logs['val']['score']:
                self.best_run = { 
                    'epoch': epoch_num, 
                    'val_score': logs['val']['score'], 
                    'train_score': logs['train']['score'] 
                }
                self._serialize_model(model_path)
                with open(os.path.join(TINY_IMAGENET_MODEL_DIR, 'best_run.dat'), 'w') as f:
                    json.dump(self.best_run, f)
        return serialize_best_model_cb
        