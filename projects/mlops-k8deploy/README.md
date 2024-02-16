# Introduction
This projects deploys a trained model to the minikube kubernetes cluster. The model is trained to predict the flower prediction based on its features - sepal length, sepal width, petal length, and petal width.

# Tools used
- Miniconda (https://conda.io/projects/conda/en/latest/user-guide/install/index.html)
- Docker* (https://docs.docker.com/engine/install/)
- minikube (https://minikube.sigs.k8s.io/docs/start/)

*minikube isn't stable when podman is used as container manager

# setup minkube


# setup project environment
We will be using conda to setup virtual environment, so make sure you install conda
Navigate to mlops-k8deploy/scripts directory
```
deactivate 
./setup-env.sh <python-version>
conda activate mlops-k8deploy_env
```

# app: flower-predictor
Restful API & sample web page to predict flower given sepal length, sepal width, petal length, and petal width.


# Build and Run app
Run iris_load_and_train.ipynb to save the trained model before running the app

Make sure you are in this project root directory
```
podman build  -f ./apps/flower-predictor/DockerFile -t mlops-k8deploy_flower-predictor:latest .

podman run -it -p 8080:8080 --rm mlops-k8deploy_flower-predictor:latest
```
*you can use docker instead of podman. I use podman as it doesn't run any daemon process - I had high memory consumption issue with it.*

```
eval $(minikube docker-env)
docker build  -f ./apps/flower-predictor/DockerFile -t mlops-k8deploy_flower-predictor:latest .
minikube dashboard --url #to access k8s dashboard
kubectl create namespace iris
kubectl config set-context --current --namespace iris
kubectl apply -f apps/flower-predictor/k8s/deployment.yml
kubectl apply -f apps/flower-predictor/k8s/service.yml
minikube service -n iris flower-predictor --url # prints the url with which you can access the service
```


# TODOs
- Separate train and inference dependencies
