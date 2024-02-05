#!/bin/bash

sudo apt install python3.8-venv

python3 -m venv ~/assignment-env

source ~/assignment-env/bin/activate

pip install pyarrow==13.0.0 torch==2.0.1 torchvision==0.15.2 tqdm==4.66.1 ray[tune]==2.7.0 mlflow==2.7.0 virtualenv

nvidia-smi 

python3 -c "import torch; print(torch.cuda.device_count())"

curl https://pyenv.run | bash

echo "export PATH=$PATH:$HOME/.pyenv/bin" >> ~/.bashrc