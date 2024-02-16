from ..train import TrainerBuilder, Trainer
from ..config import TINY_IMAGENET_DATA_DIR
from ..data import TinyImageNetDataset
from ..metrics import accuracy_fn
from ..model import TinyImageNet
from .base_pipeline import BasePipeline

from torchvision import transforms
from torch.utils.data import DataLoader
from torch.optim import Adam
from torch.optim.lr_scheduler import ReduceLROnPlateau

import torch.nn.functional as F

    
class SingleThreadTrainPipeline(BasePipeline):
    def __init__(self) -> None:
        super(SingleThreadTrainPipeline, self).__init__()
    
    def train(self, epochs: int):
        self._init_model()
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
            .build()
        
        logs = trainer.train(self.train_data, self.val_data, epochs)
        print(f"last epoch's -> {logs}")
    
    def test(self):
        self._init_test_data()
        trainer = TrainerBuilder() \
            .model(self.model) \
            .metric_fn(accuracy_fn) \
            .build()
        loss, accuracy = trainer.test(self.test_data)
        print(f"test accuracy={accuracy}")
    
    def run(self, train_epochs: int):
        self.train(train_epochs)
        