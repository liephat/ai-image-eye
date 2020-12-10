import cv2
import pandas as pd
import rawpy
import os
from tqdm import tqdm
from app.util.config_parser import ConfigParser
from app.util.model import ResNet

# Load application configurations
Config = ConfigParser()

# Load ResNet model
ResNet = ResNet(Config.model('resnet'), Config.labels('resnet'))
ResNet.load()

# Create data frame to save image labels
data = pd.DataFrame(columns=['file', 'labels'])
data.index.name = 'uid'

for row, image_path in enumerate(tqdm(Config.image_files())):

    file_ending = os.path.splitext(image_path)[1].lower()
    if file_ending == 'arw':
        with rawpy.imread(image_path) as raw:
            image = raw.post_process()
    else:  # if file_ending in ['jpg', 'jpeg']:
        image = cv2.imread(image_path)

    labels = ResNet.classify(image)

    # get relative path to image
    rel_path = os.path.relpath(image_path, Config.image_folder())

    # create new row in data frame for image with path and top-5 labels
    data.loc[row] = [rel_path] + [labels]

    # persist row
    data.to_csv('data.csv')
