import os

import cv2
import rawpy
from tqdm import tqdm

from app.data.ops import ImageDataHandler
from app.labeling.model import ResNet
from app.config.parser import ConfigParser

# Load application configurations
config = ConfigParser()

# Load ResNet model
res_net = ResNet(config.model('resnet'), config.labels('resnet'))
res_net.load()


for row, image_path in enumerate(tqdm(config.image_files())):

    file_ending = os.path.splitext(image_path)[1].lower()
    if file_ending == 'arw':
        with rawpy.imread(image_path) as raw:
            image = raw.post_process()
    else:  # if file_ending in ['jpg', 'jpeg']:
        image = cv2.imread(image_path)  # pylint: disable=no-member

    labels = res_net.classify(image)

    # get relative path to image
    rel_path = os.path.relpath(image_path, config.image_folder())

    # create new row in data frame for image with path and top-5 labels
    for label in labels:
        ImageDataHandler.add_label_assignment(rel_path, label, 'ResNet_ImageNet')
