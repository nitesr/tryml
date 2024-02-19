from .single_thread import SingleThreadTrainPipeline

from torch import nn
import torch

class DataParallelTrainPipeline(SingleThreadTrainPipeline):
    def __init__(self) -> None:
        super(DataParallelTrainPipeline, self).__init__()
    
    def run(
        self, train_epochs: int, 
        cuda_devices=None, train_device=None, 
        memory_limit=None, init_model=False):
        
        self._load_model(init_model)
        dc = torch.cuda.device_count()
        
        if cuda_devices is None:    
            cuda_devices = [n for n in range(0, dc)] if dc > 1 else dc
        self.model = nn.DataParallel(self.model, cuda_devices)
        
        if memory_limit is not None:
            torch.cuda.set_per_process_memory_fraction(memory_limit)
        
        if train_device is not None:
            self.model = self.model.to(torch.device(train_device))
        
        print(
            f'cuda available={torch.cuda.is_available()}',
            f'cuda device_count={torch.cuda.device_count()}', 
            f'cuda_devices={cuda_devices}',
            f'train_device={train_device}')
        
        self._download_dataset()
        self.train(train_epochs, train_device)
        self.test(train_device)
        
        def cal_max_mem(d) -> float:
            mem = torch.cuda.max_memory_allocated(d)
            return round(mem / 1024 / 1024, 2)
            
        devices_max_mem = [ str(cal_max_mem(d))+f'MB on device-{d}'  for d in range(dc)]
        print(f'max memory allocated = {devices_max_mem}')