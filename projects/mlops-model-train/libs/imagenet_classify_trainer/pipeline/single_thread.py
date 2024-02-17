from ..train import TrainerBuilder, Trainer
from ..config import TINY_IMAGENET_DATA_DIR
from ..config import TINY_IMAGENET_BEST_MODEL_PATH
from ..data import TinyImageNetDataset
from ..metrics import accuracy_fn
from ..model import TinyImageNet
from .base_pipeline import BasePipeline

from torchvision import transforms
from torch.utils.data import DataLoader
from torch.optim import Adam
from torch.optim.lr_scheduler import ReduceLROnPlateau

import torch.nn.functional as F
import os

class SingleThreadTrainPipeline(BasePipeline):
    def __init__(self) -> None:
        super(SingleThreadTrainPipeline, self).__init__()
    
    def train(self, epochs: int=5):
        self._init_train_data()
        self._init_val_data()
        
        optimizer = Adam(self.model.parameters(), lr=0.001)
        lr_scheduler = ReduceLROnPlateau(optimizer, mode="min", patience=10, factor=0.05, min_lr=0.00001)
        trainer = TrainerBuilder() \
            .model(self.model) \
            .loss_fn(F.cross_entropy) \
            .optim(optimizer) \
            .lr_schedule(lr_scheduler) \
            .metric_fn(accuracy_fn) \
            .add_callback(self._get_serialize_best_model_cb()) \
            .build()
        
        logs = trainer.train(self.train_data, self.val_data, epochs)
        print(f"last epoch's -> {logs}")
    
    def test(self):
        self._init_test_data()
        trainer = TrainerBuilder() \
            .model(self.model) \
            .loss_fn(F.cross_entropy) \
            .metric_fn(accuracy_fn) \
            .build()
        _, accuracy, _ = trainer.test(self.test_data)
        print(f"test accuracy={accuracy}")
    
    def run(self, train_epochs: int, init_model=False):
        self._init_model()
        if not init_model and os.path.exists(TINY_IMAGENET_BEST_MODEL_PATH):
            self._deserialize_model(TINY_IMAGENET_BEST_MODEL_PATH)
            
        self._download_dataset()
        self.train(train_epochs)
        self.test()
        