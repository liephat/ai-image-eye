from abc import abstractmethod
import numpy as np
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
    def _preprocess():
        pass

    @staticmethod
    @abstractmethod
    def _postprocess():
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
