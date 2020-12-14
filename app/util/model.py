from abc import abstractmethod
import numpy as np
import cv2
import onnxruntime


class Model:
    """
    Baseclass for all machine learning models. The class is used to implement concrete model classes
    instantiating sessions based on ONNX format models and classifying images in the instantiated
    session.
    """

    def __init__(self, model, labels):
        """
        :param model: filename with ONNX format containing trained model
        :param labels: json file containing output label dictionary
        """
        self.model = model
        self.labels = labels
        self.session = None

    def load(self):
        """
        Starts an inference session in ONNX runtime.
        """
        # Run the model on the backend
        self.session = onnxruntime.InferenceSession(self.model, None)

    @staticmethod
    @abstractmethod
    def pre_process():
        pass

    @staticmethod
    @abstractmethod
    def post_process():
        pass

    @abstractmethod
    def classify(self, img):
        """
        Returns predicted output class labels for an image.

        :param img: image file with content that shall be labeled
        :return: dictionary with probabilities as keys and predicted output classes as values
        """
        pass

    @staticmethod
    def softmax(x):
        """
        Normalizes the output of a model to a probability distribution over all predicted output
        classes.

        :param x: output of the last layer of a network model
        :return: probability distribution over the predicted output classes
        """
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum(axis=0)


class ResNet(Model):

    def classify(self, img):
        # get the name of the first input of the labeling
        input_name = self.session.get_inputs()[0].name

        # set preprocessed image as input and compute predictions
        input_data = ResNet.pre_process(img)
        raw_result = self.session.run([], {input_name: input_data})
        raw_result = np.array(raw_result).reshape(-1)

        # post process raw result; essentially consists of performing a softmax function
        result = ResNet.post_process(raw_result)

        # get indices that sort the result list, remove its single dimensions and reverse its order
        sorted_ids = np.flip(np.squeeze(np.argsort(result)))

        # Create dictionary with probabilities as keys and labels as values for top 5 predictions
        labels = dict(zip(self.labels[sorted_ids[:5]], raw_result[sorted_ids[:5]]))

        return labels

    @staticmethod
    def post_process(result):
        return Model.softmax(np.array(result)).tolist()

    @staticmethod
    def pre_process(img):
        # resize image to input size of resnet
        img = cv2.resize(img, (224, 224))  # pylint: disable=no-member

        # convert HxWxC to a CxHxW tensor
        img_data = np.array(img).transpose(2, 0, 1)

        # convert image data into the float32 input
        img_data = img_data.astype('float32')

        # normalize image data
        m = np.array([0.485, 0.456, 0.406])
        std = np.array([0.229, 0.224, 0.225])
        norm_img_data = np.zeros(img_data.shape).astype('float32')
        for i in range(img_data.shape[0]):
            norm_img_data[i, :, :] = (img_data[i, :, :] / 255 - m[i]) / std[i]

        # add batch channel, result is a NxCxHxW tensor
        norm_img_data = norm_img_data.reshape(1, 3, 224, 224).astype('float32')  # pylint: disable=too-many-function-args
        return norm_img_data
