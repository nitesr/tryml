import os
import torch.distributed as dist
import torch.multiprocessing as mp

def init_process(rank, size, fn, backend='gloo', host='localhost', port=29500):
    os.environ['MASTER_ADDR'] = host
    os.environ['MASTER_PORT'] = str(port)
    
    if backend == 'gloo':
        # for my macbook to resolve Warning
        #   Warning: Unable to resolve hostname to a (local) address. 
        #   Using the loopback address as fallback. Manually set the network interface 
        #       to bind to with GLOO_SOCKET_IFNAME. (function operator()) 
        os.environ['GLOO_SOCKET_IFNAME'] = 'en0' 
    
    print(
        'initializing process',  f', process={mp.current_process()}'
        f'backend={backend}, rank={rank}, world_size={size}')
    dist.init_process_group(backend, rank=rank, world_size=size)
    fn(rank, size)