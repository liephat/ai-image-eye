import os

import cv2
import rawpy
import numpy as np
from tqdm import tqdm

from app.data.ops import ImageDataHandler
from app.labeling.res_net import ResNet
from app.labeling.yolo_v4 import YoloV4
from app.config.parser import ConfigParser


def run_classifiers(config: ConfigParser):

    # Load ResNet model
    res_net = ResNet(config.model('resnet'), config.labels('resnet'))
    res_net.load()

    # Load YoloV4 model
    yolo_v4 = YoloV4(config.model('yolov4'), config.labels('yolov4'))
    yolo_v4.load()


    for row, image_path in enumerate(tqdm(config.image_files())):

        file_ending = os.path.splitext(image_path)[1].lower()
        if file_ending == 'arw':
            with rawpy.imread(image_path) as raw:
                image = raw.post_process()
        else:  # if file_ending in ['jpg', 'jpeg']:
            image = cv2.imread(image_path)  # pylint: disable=no-member

        # get relative path to image
        rel_path = os.path.relpath(image_path, config.image_folder())

        # classify image with resnet
        labels, confidences = res_net.classify(np.copy(image))

        # create new entry in database for image with relative path and top-5 labels
        for (label, confidence) in zip(labels, confidences):
            ImageDataHandler.add_label_assignment(rel_path, label, 'ResNet_ImageNet', confidence)

        # classify image with yolov4
        labels, confidences, bounding_boxes = yolo_v4.classify(np.copy(image))

        for (label, confidence, bounding_box) in zip(labels, confidences, bounding_boxes):
            ImageDataHandler.add_label_assignment(rel_path, label, 'YoloV4_COCO', confidence,
                                                  repr(bounding_box))

if __name__ == '__main__':
    # Load application configurations
    config = ConfigParser()

    if os.path.exists(config.data_file()):
        os.remove(config.data_file())

    run_classifiers(config)