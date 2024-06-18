# Introduction
Supervised Learning I

# Tools used
- Miniconda (https://conda.io/projects/conda/en/latest/user-guide/install/index.html)
- Podman or Docker

# setup project environment
We will be using conda to setup virtual environment, so make sure you install conda
Navigate to supervised1/scripts directory
```
deactivate de
./setup-env.sh 3.12
conda activate supervised1_env
```

# app: supervised1
supervised1

# Build and Run app
Make sure you are in this project root directory
```
podman build  -f ./apps/supervised1/DockerFile -t supervised1_supervised1:latest .

podman run -it -p 8080:8080 --rm supervised1_supervised1:latest
```
*you can use docker instead of podman. I use podman as it doesn't run any daemon process - I had high memory consumption issue with it.*

# TODOs
- Separate train and inference dependencies
