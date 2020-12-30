import os

import cv2
import pandas as pd
import rawpy
from tqdm import tqdm

from app.data.ids import create_id
from app.labeling.model import ResNet
from app.util.config_parser import ConfigParser

# Load application configurations
Config = ConfigParser()

# Load ResNet model
ResNet = ResNet(Config.model('resnet'), Config.labels('resnet'))
ResNet.load()

# Create data frame to save image labels
data = pd.DataFrame(columns=['uid', 'file', 'labels'])
data.index.name = 'id'

for row, image_path in enumerate(tqdm(Config.image_files())):

    uid = create_id()

    file_ending = os.path.splitext(image_path)[1].lower()
    if file_ending == 'arw':
        with rawpy.imread(image_path) as raw:
            image = raw.post_process()
    else:  # if file_ending in ['jpg', 'jpeg']:
        image = cv2.imread(image_path)  # pylint: disable=no-member

    labels = ResNet.classify(image)

    # get relative path to image
    rel_path = os.path.relpath(image_path, Config.image_folder())

    # create new row in data frame for image with path and top-5 labels
    data.loc[row] = [uid] + [rel_path] + [labels]

    # persist row
    data.to_csv('data.csv')
