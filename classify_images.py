import numpy as np
import onnxruntime
import json
import cv2
import rawpy
import pandas as pd
from tqdm import tqdm
from config.parser import ConfigParser


def load_raw_image(path):
    with rawpy.imread(path) as raw:
        rgb = raw.postprocess()
    return rgb


def preprocess(img):
    # resize image to input size of resnet
    img = cv2.resize(img, (224, 224))

    # convert HxWxC to a CxHxW tensor
    img_data = np.array(img).transpose(2, 0, 1)

    # convert image data into the float32 input
    img_data = img_data.astype('float32')

    # normalize image data
    m_vec = np.array([0.485, 0.456, 0.406])
    std_vec = np.array([0.229, 0.224, 0.225])
    norm_img_data = np.zeros(img_data.shape).astype('float32')
    for i in range(img_data.shape[0]):
        norm_img_data[i, :, :] = (img_data[i, :, :] / 255 - m_vec[i]) / std_vec[i]

    # add batch channel, result is a NxCxHxW tensor
    norm_img_data = norm_img_data.reshape(1, 3, 224, 224).astype('float32')
    return norm_img_data


def softmax(x):
    x = x.reshape(-1)
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)


def postprocess(result):
    return softmax(np.array(result)).tolist()


Config = ConfigParser()

# Run the model on the backend
session = onnxruntime.InferenceSession(Config.model(), None)

# Get the name of the first input of the model
input_name = session.get_inputs()[0].name

labels = Config.labels()

data = pd.DataFrame(columns=['File', 'ResNet50-1', 'ResNet50-2', 'ResNet50-3', 'ResNet50-4', 'ResNet50-5'])
row = 0

for image_path in tqdm(Config.image_files()):

    file_ending = image_path[-3:]
    if file_ending == 'ARW':
        image = load_raw_image(image_path)
    elif file_ending == 'jpg':
        image = cv2.imread(image_path)

    input_data = preprocess(image)
    raw_result = session.run([], {input_name: input_data})

    # raw_result = np.array(raw_result).reshape(-1)

    result = postprocess(raw_result)

    idx = np.argmax(result)
    sort_idx = np.flip(np.squeeze(np.argsort(result)))

    # top_labels = zip(raw_result[sort_idx[:5]], labels[sort_idx[:5]])

    data.loc[row] = [image_path] + list(labels[sort_idx[:5]])
    data.to_csv('data.csv')
    row += 1
