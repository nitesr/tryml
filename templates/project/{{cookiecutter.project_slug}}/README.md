# Introduction
{{ cookiecutter.project_description }}

# Tools used
- Miniconda (https://conda.io/projects/conda/en/latest/user-guide/install/index.html)
- Podman or Docker

# setup project environment
We will be using conda to setup virtual environment, so make sure you install conda
Navigate to {{ cookiecutter.project_name }}/scripts directory
```
deactivate 
./setup-env.sh <python-version>
conda activate {{ cookiecutter.project_name }}_env
```

# app: {{ cookiecutter.app_name }}
{{ cookiecutter.app_description }}

# Build and Run app
Make sure you are in this project root directory
```
podman build  -f ./apps/{{ cookiecutter.app_name }}/DockerFile -t {{ cookiecutter.project_slug }}_{{ cookiecutter.app_name }}:latest .

podman run -it -p 8080:8080 --rm {{ cookiecutter.project_slug }}_{{ cookiecutter.app_name }}:latest
```
*you can use docker instead of podman. I use podman as it doesn't run any daemon process - I had high memory consumption issue with it.*

# TODOs
- Separate train and inference dependencies
