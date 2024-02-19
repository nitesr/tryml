import torch.distributed as dist
import torch

from torchvision import transforms, datasets
from torch.utils.data import DataLoader, random_split

from ..config import DATA_DIR
from .data_partition import DataPartitioner

def minst_partition_dataset(batch_size=128, seed=1234):
    img_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    
    ds = datasets.MNIST(
        DATA_DIR, train=True, download=True,
        transform=img_transform)
    ds_lst = random_split(
        ds, lengths=[0.8, 0.2], 
        generator=torch.Generator().manual_seed(seed))
    
    size = dist.get_world_size()
    bsz = int(batch_size / size)
    partition_sizes = [1.0 / size for _ in range(size)]
    partitioner = DataPartitioner(ds_lst[0], partition_sizes, seed=seed)
    partition = partitioner.use(dist.get_rank())
    train_set = DataLoader(partition, batch_size=bsz, shuffle=True)
    test_set = DataLoader(ds_lst[1], batch_size=bsz, shuffle=True)
    return train_set, test_set, bsz