from .ddataset import minst_partition_dataset
from .models import MinstNet
from .initproc import init_process

from torch import optim
from torch.nn import functional as F
from math import ceil

import torch
import torch.distributed as dist
import torch.multiprocessing as mp

def average_gradients(model):
    all_group = dist.new_group([p for p in range(dist.get_world_size())])
    dist.barrier(all_group)
    
    for param in model.parameters():
        dist.all_reduce(param.grad.data, op=dist.ReduceOp.SUM, group=all_group)
        param.grad.data /= float(dist.get_world_size())

def test(model, dl):
    model.eval()
    test_loss = 0
    correct = 0
    num_batches = 0
    with torch.no_grad():
        for data, target in dl:
            output = model(data)
            loss = F.nll_loss(output, target)
            test_loss += loss.item()
            pred = output.argmax(dim=1, keepdim=True)
            correct += pred.eq(target.view_as(pred)).sum().item()
            num_batches += 1
    return test_loss / len(dl), 100. * correct / len(dl.dataset)

def train_epoch(model, dl, optimizer):
    model.train()
    epoch_loss = 0.0
    for data, target in dl:
        optimizer.zero_grad()
        output = model(data)
        loss = F.nll_loss(output, target)
        epoch_loss += loss.item()
        loss.backward()
        average_gradients(model)
        optimizer.step()
    return epoch_loss / len(dl)
        
def run(rank, size):
    torch.manual_seed(1234)
    train_set, test_set, local_batch_size = minst_partition_dataset(batch_size=128, seed=1234)
    print(
        'Rank ', dist.get_rank(),
        f', len: train={len(train_set)}, test={len(test_set)}',
        f', local_batch_size={local_batch_size}')
    
    model = MinstNet()
    optimizer = optim.SGD(
        model.parameters(),
        lr=0.01, momentum=0.5)
    
    for epoch in range(4):
        epoch_loss = train_epoch(model, train_set, optimizer)
        test_loss, test_acc = test(model, test_set)
        
        print('Rank ', dist.get_rank(), ', epoch ',
              epoch, ': ', epoch_loss, 
              ', test_loss :', test_loss,
              ', test_accuracy :', test_acc)

if __name__ == "__main__":
    size = 4
    mp.spawn(
        init_process, args=(size, run), nprocs=size, 
        join=True, daemon=False, 
        start_method='spawn')