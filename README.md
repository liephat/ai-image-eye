# ai-image-eye
![Demo](media/demo.gif)

A responsive image gallery with an AI powered backend labeling the content. 

The server application crawls through a user-defined folder searching for images. The images are then scanned by a 
set of deep learning models providing labels describing the images. The labels are finally stored in a SQL database.

AI labeling features:
- Image classification 
- Object detection
- Face recognition

The image gallery can be accessed via browser. The images are provided by a react-app communicating through a 
REST API with a backend based on python flask.

## Requirements

Run ```pip install -r requirements.txt``` in project directory.

## Some information

ResNet source: https://github.com/onnx/models/blob/master/vision/classification/resnet/model/resnet50-v2-7.onnx

YoloV4 source: https://github.com/onnx/models/blob/master/vision/object_detection_segmentation/yolov4/model/yolov4.onnx

## Run instructions (Backend: flask-app)
Make sure you are using git-lfs to pull the large deep learning model files. The path to the directory of your images 
must be defined in ```config/settings.json```.

Run ```python classify_images.py```. The script scans for images and writes their labels to a SQL database saved in 
```config/image_label.db```.

Run ```python -m app``` to start the image server.


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
sudo docker run -p 5050:80 --memory=1g imagegallery
```
