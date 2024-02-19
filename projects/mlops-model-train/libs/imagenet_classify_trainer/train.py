import torch, tqdm
import numpy as np

class Trainer :
    def __init__(self) -> None:
        self._set_defaults()
    
    def _check_if_exist(self, attr_name) -> bool:
        return hasattr(self, attr_name) and getattr(self, attr_name) is not None
    
    def _set_defaults(self) -> None:
        if not self._check_if_exist('device'):
            self.device = torch.device('cpu')
        
        if not self._check_if_exist('callbacks'):
            self.callbacks = []
        
        if not self._check_if_exist('metric_fn'):
            self.metric_fn = lambda p, t: 0
        
        class MockLRScheduler:
            def __init__(self) -> None:
                pass
            
            def step(self, *args) -> None:
                pass
            
        if not self._check_if_exist('lr_scheduler'):
            self.lr_scheduler = MockLRScheduler()
        
    def __validate(self) -> None:
        assert self.model
        assert self.loss_fn
        assert self.optimizer
        assert self.device
        assert self.metric_fn
        assert self.lr_scheduler
    
    def _train_epoch(self, data):
        self.model.train()
        batch_loss_sum = 0
        batch_metric_sum = 0
        
        for X, Y in tqdm.tqdm(data):
            X = X.to(self.device)
            Y = Y.to(self.device)
            
            self.optimizer.zero_grad()
            
            logits = self.model(X)
            loss = self.loss_fn(logits, Y)
            batch_loss_sum += loss.item()
            batch_metric_sum += self.metric_fn(logits.detach(), Y)
            loss.backward()
            
            self.optimizer.step()
        
        return batch_loss_sum/len(data), batch_metric_sum/len(data)

    def train(self, train_data, val_data=None, epochs=1):
        self.__validate()
        self.model = self.model.to(self.device)
        
        logs = {}
        for epoch_num in tqdm.tqdm(range(1, epochs+1)):
            train_epoch_loss, train_epoch_score = self._train_epoch(train_data)
            val_loss, val_score = (0, 0)
            if val_data is not None:
                val_loss, val_score, _ = self.test(val_data)
                self.lr_scheduler.step(val_loss)
            else:
                self.lr_scheduler.step(train_epoch_loss)
            
            logs = {
                'train': {'loss': train_epoch_loss, 'score': train_epoch_score},
                'val': {'loss': val_loss, 'score': val_score}
            }
            for cb in self.callbacks:
                cb(epoch_num, logs)
        return logs
    
    def _validate_for_test(self):
        assert self.model
        assert self.device
        assert self.loss_fn
        assert self.metric_fn
        
    def test(self, data):
        self._validate_for_test()
        self.model.eval()
        
        batch_metric_sum = 0
        batch_loss_sum = 0
        Y_pred = []
        with torch.no_grad():
            for X, Y in tqdm.tqdm(data):
                X = X.to(self.device)
                Y = Y.to(self.device)
                logits = self.model(X)
                loss = self.loss_fn(logits, Y)
                batch_loss_sum += loss.item()
                batch_metric_sum += self.metric_fn(logits.detach(), Y)
                Y_pred.extend(torch.argmax(logits.detach(), 1).tolist())
            
        return batch_loss_sum/len(data), batch_metric_sum/len(data), np.array(Y_pred)

# from typing import Self # only from python 3.11

class TrainerBuilder :
    def __init__(self) -> None:
        self.trainer = Trainer()
        self.trainer.callbacks = []
    
    def model(self, model) : # -> Self:
        self.trainer.model = model
        return self
    
    def loss_fn(self, loss_fn) : # -> Self:
        self.trainer.loss_fn = loss_fn
        return self
    
    def optim(self, optimizer) : # -> Self:
        self.trainer.optimizer = optimizer
        return self
    
    def lr_schedule(self, lr_scheduler) : # -> Self:
        self.trainer.lr_scheduler = lr_scheduler
        return self
    
    def metric_fn(self, metric_fn) : # -> Self:
        self.trainer.metric_fn = metric_fn
        return self
    
    def device(self, device) : # -> Self:
        self.trainer.device = torch.device('cpu') if device is None else device
        return self
    
    def add_callback(self, cb_fn) : # -> Self:
        self.trainer.callbacks.append(cb_fn)
        return self
    
    def build(self) -> Trainer:
        return self.trainer