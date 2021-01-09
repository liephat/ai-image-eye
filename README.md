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

## Run instructions
Make sure you have saved the ResNet model and its label dictionary to a directory, e.g. ```/config/models/resnet```. 
The paths to these files and the path to the directory of your images must be defined in ```/config/settings.json```.

Run ```python classify_images.py```. The script creates a file ```data.csv``` containing the Top-5 labels for each image
in your image directory.

Run ```python -m app``` to start the application.


## REST API

The REST API can be reached under the endpoint `/api`. A documentation
including a Swagger UI is created automatically under `/api/doc`.

### Useful endpoints:

- `/api/images/all` ... Get all imagess

