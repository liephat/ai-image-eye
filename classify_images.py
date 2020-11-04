import cv2
import pandas as pd
import rawpy
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

for row, image_path in enumerate(tqdm(Config.image_files())):

    file_ending = image_path[-3:].lower()
    if file_ending == 'arw':
        with rawpy.imread(image_path) as raw:
            image = raw.post_process()
    elif file_ending == 'jpg':
        image = cv2.imread(image_path)

    labels = ResNet.classify(image)

    # create new row in data frame for image with path and top-5 labels
    data.loc[row] = [image_path] + [labels]

    # persist row
    data.to_csv('data.csv')
