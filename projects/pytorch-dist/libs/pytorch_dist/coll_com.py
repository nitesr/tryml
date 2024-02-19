#!/usr/bin/env python
import torch
import torch.distributed as dist
import torch.multiprocessing as mp
from .initproc import init_process

def run(rank, size):
    group = dist.new_group([pIdx for pIdx in range(size)])
    tensor = torch.ones(1)
    dist.all_reduce(tensor, op=dist.ReduceOp.SUM, group=group)
    print('Rank ', rank, ' has data ', tensor[0])

if __name__ == "__main__":
    size = 2
    mp.spawn(
        init_process, args=(size, run), nprocs=size, 
        join=True, daemon=False, 
        start_method='spawn')