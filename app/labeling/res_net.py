import cv2
import numpy as np

from app.labeling.model import Model


class ResNet(Model):

    def classify(self, image):
        # get the name of the first input of the labeling
        input_name = self.session.get_inputs()[0].name

        # set preprocessed image as input and compute predictions
        input_data = ResNet._preprocess(image)
        raw_result = self.session.run([], {input_name: input_data})
        raw_result = np.array(raw_result).reshape(-1)

        # post process raw result; essentially consists of performing a softmax function
        result = ResNet._postprocess(raw_result)

        # get indices that sort the result list, remove its single dimensions and reverse its order
        sorted_ids = np.flip(np.squeeze(np.argsort(result)))

        # Create dictionary with probabilities as keys and labels as values for top 5 predictions
        # labels = dict(zip(self.labels[sorted_ids[:5]], raw_result[sorted_ids[:5]]))
        labels = self.labels[sorted_ids[:5]]

        return labels

    @staticmethod
    def _postprocess(raw_result):
        return Model.softmax(np.array(raw_result)).tolist()

    @staticmethod
    def _preprocess(image):
        # resize image to input size of resnet
        image = cv2.resize(image, (224, 224))  # pylint: disable=no-member

        # convert HxWxC to a CxHxW tensor
        image_data = np.array(image).transpose(2, 0, 1)

        # convert image data into the float32 input
        image_data = image_data.astype('float32')

        # normalize image data
        mean = np.array([0.485, 0.456, 0.406])
        standard_deviation = np.array([0.229, 0.224, 0.225])
        normalized_image_data = np.zeros(image_data.shape).astype('float32')
        for i in range(image_data.shape[0]):
            normalized_image_data[i, :, :] = (image_data[i, :, :] / 255 - mean[i]) / standard_deviation[i]

        # add batch channel, result is a NxCxHxW tensor
        normalized_image_data = normalized_image_data.reshape(1, 3, 224, 224).astype('float32')  # pylint: disable=too-many-function-args
        return normalized_image_data
