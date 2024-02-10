# Introduction
This project demonstrates exposing an RESTful API on trained model (to classify dog vs cat) and packaging for deployment.

# Tools used
Python 3.7
Tensorflow
Flask
gunicorn
Docker

# Dog Cat Classifier
This is a Dog Cat Classifier that uses image classification to distinguish between images of dogs and cats.

# Build and Run app
Make sure you are in this project root directory
```
podman build  -f ./apps/cats_dogs_classifier/DockerFile -t mlops_dogcatclassifier:latest .

podman run -it -p 8080:8080 --rm mlops_dogcatclassifier:latest
```
*you can use docker instead of podman. I use podman as it doesn't run any daemon process - I had high memory consumption issue with it.*

# TODOs
- Separate train and inference dependencies
