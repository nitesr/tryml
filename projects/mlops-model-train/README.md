# Introduction
This project is to use AWS EC2, MLFlow, Raytune, FSDP and train classification/localization model on tiney imagenette dataset

# Tools used

# setup project environment
We will be using conda to setup virutal environment, so make sure you install conda
Navigate to mlops-model-train/scripts directory
```
deactivate 
./setup-env.sh <python-version>
conda activate mlops-model-train_env
```

# app: imagenet_objdetector 
imagenet_objdetector 

# Build and Run app
Make sure you are in this project root directory
```
podman build  -f ./apps/imagenet_objdetector /DockerFile -t mlops-model-train_imagenet_objdetector :latest .

podman run -it -p 8080:8080 --rm mlops-model-train_imagenet_objdetector :latest
```
*you can use docker instead of podman. I use podman as it doesn't run any daemon process - I had high memory consumption issue with it.*

# References
https://www.vldb.org/pvldb/vol13/p3005-li.pdf - Pytorch DDP
https://pytorch.org/tutorials/intermediate/dist_tuto.html

Parmeter averaging ?

# TODOs
- Understanding the DDP with a naive model with micro-batches. Particulary to notice how parameters will be same across the devices (each local fwd-bwd pass with no_sync should change the parameters)
