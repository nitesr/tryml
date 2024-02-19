# Introduction
This project is to try out the samples from pytorch distributed docs

# Tools used
- Miniconda (https://conda.io/projects/conda/en/latest/user-guide/install/index.html)
- Podman or Docker

# setup project environment
We will be using conda to setup virtual environment, so make sure you install conda
Navigate to pytorch-dist/scripts directory
```
deactivate 
./setup-env.sh <python-version>
conda activate pytorch-dist_env
```

# app: pytorch-dist
pytorch-dist

# Build and run python scripts
Make sure you are in this project root directory
```
conda activate pytorch-dist_env
pip install -e libs
```

# coll_com.py
```
python -m pytorch_dist.coll_com
```

# dist_train.py
Note: 
- if you face any issues with too many open files. run ```ulimit -n 65535``` 
- if you get any warning on hostname, make sure you get the ethernet interfaces using command `ifconfig` and set the name e.g. 'eth0' against env-var GLOO_SOCKET_IFNAME in initproc.py
```
python -m pytorch_dist.dist_train
```

# Build and Run app
Make sure you are in this project root directory
```
podman build  -f ./apps/pytorch-dist/DockerFile -t pytorch-dist_pytorch-dist:latest .

podman run -it -p 8080:8080 --rm pytorch-dist_pytorch-dist:latest
```
*you can use docker instead of podman. I use podman as it doesn't run any daemon process - I had high memory consumption issue with it.*

# TODOs
- Separate train and inference dependencies
