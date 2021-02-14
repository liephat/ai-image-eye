# flask-image-database

A responsive image gallery based on python flask. The aim of this application is to provide an automatic labeling of objects
and scenes in images and present them in a gallery that can be accessed by any web browser. It should additionally be possible
to filter the image collection according to labels that were automatically determined by running pretrained classification models on the
whole dataset.

Work is currently in progress.

There are some features yet to be developed:
- Running application in a customized docker container
- Dynamic loading of images
- Rest API communication between backend and frontend
- Frontend filter functionality
- Automatic job that runs periodically to classify images
- Appropriate form of persisting detected labels

## Requirements

Run ```pip install -r requirements.txt``` in project directory.

## Some information

ResNet source: https://github.com/onnx/models/blob/master/vision/classification/resnet/model/resnet50-v2-7.onnx


## Run instructions (Backend: flask-app)
Make sure you have saved the ResNet model and its label dictionary to a directory, e.g. ```/config/models/resnet```. 
The paths to these files and the path to the directory of your images must be defined in ```/config/settings.json```.

Run ```python classify_images.py```. The script creates a file ```data.csv``` containing the Top-5 labels for each image
in your image directory.

Run ```python -m app``` to start the application.


## Run instructions (Frontend: react-app)

See [react-app README](react-app/README.md)


## REST API

The REST API can be reached under the endpoint `/api`. A documentation
including a Swagger UI is created automatically under `/api/doc`.

### Useful endpoints:

- `/api/images/all` ... Get all imagess

# Docker

The Docker image is based on an nginx image that will contain

* The Flask backend served on port 80 at the root
* The React App frontend at URL `/static/ui`

The following volumes need to be mounted:

* `config`: contains the settings.json, image database and image processing models
* `images`: directory with images

This is taken care of in `docker-compose.yml`.

## Create Docker image

Before creating the Docker image, the React App should be packaged for deployment using `yarnpkg build`.

```shell script
sudo docker build -t imagegallery:latest .
```

See `build-docker.sh`.

## Run Docker image
### via docker-compose

```shell script
sudo docker-compose up
```

### directly with docker run
*not recommended, because volumes not specified. Better use docker-compose*

```shell script
sudo docker run -p 5000:80 --memory=1g imagegallery
```
