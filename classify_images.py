import json
import os

import cv2
import rawpy
import numpy as np
from tqdm import tqdm
import face_recognition

from app.data.ops import ImageDataHandler
from app.labeling.res_net import ResNet
from app.labeling.yolo_v4 import YoloV4
from app.config.parser import ConfigParser
from app.utils.helper import normalize_coordinates


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

        origin = 'ResNet:ImageNet'
        if not ImageDataHandler.get_assignments_from_origin(rel_path, origin):
            # classify image with resnet
            labels, confidences = res_net.classify(np.copy(image))

            # create new entry in database for image with relative path and top-5 labels
            for (label, confidence) in zip(labels, confidences):
                ImageDataHandler.add_label_assignment(rel_path, label_name=label, origin_name=origin,
                                                      confidence=confidence)

        origin = 'YoloV4:COCO'
        if not ImageDataHandler.get_assignments_from_origin(rel_path, origin):
            # classify image with yolov4
            labels, confidences, bounding_boxes = yolo_v4.classify(np.copy(image))

            for (label, confidence, bounding_box) in zip(labels, confidences, bounding_boxes):
                ImageDataHandler.add_label_assignment(rel_path, label_name=label, origin_name=origin,
                                                      confidence=confidence, bounding_boxes=repr(bounding_box))

        origin = 'dlib_face_rec'
        if not ImageDataHandler.get_assignments_from_origin(rel_path, origin):
            scale_percent = 25  # percent of original size
            width = int(image.shape[1] * scale_percent / 100)
            height = int(image.shape[0] * scale_percent / 100)
            dim = (width, height)

            # resize image
            image_resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

            # classify image with face_recognition
            bboxes = face_recognition.face_locations(image_resized, model='hog')
            encodings = face_recognition.face_encodings(image_resized)

            for (bbox, encoding) in zip(bboxes, encodings):
                coor_orig = np.array([bbox[0], bbox[3], bbox[2], bbox[1]])  # top, left, bottom, right
                coor = normalize_coordinates(coor_orig, image_resized)
                bounding_box = ((coor[0], coor[1]), (coor[2], coor[3]))
                ImageDataHandler.add_label_assignment(rel_path, label_name='unknown_face',
                                                      origin_name=origin, bounding_boxes=repr(bounding_box),
                                                      encoding=json.dumps(list(encoding)), editable=True)


if __name__ == '__main__':
    # Load application configurations
    config = ConfigParser()

    run_classifiers(config)
