import json
import glob
import os
import numpy as np

FILE = 'config/settings.json'


class ConfigParser:
    """
    Parses settings from a config file.
    """

    def __init__(self):
        self.settings = None
        self.read(FILE)

    def read(self, file):
        with open(file) as f:
            self.settings = json.load(f)

    def image_folder(self):
        path = self.settings['images']['folder']
        if not os.path.isabs(path):
            path = os.path.join(os.getcwd(), path)
        return path

    def image_formats(self):
        return self.settings['images']['formats']

    def image_files(self):
        fp = []
        for ff in self.image_formats():
            fp += glob.glob(os.path.join(self.image_folder(), '**', f'*.{ff}'), recursive=True)
        return fp

    def model(self, _type):
        return self.settings['labeling'][_type]['model']

    def labels(self, _type):
        with open(self.settings['labeling'][_type]['labels']) as f:
            data = json.load(f)
        return np.asarray(data)

    def data_file(self):
        return self.settings['data']['file']
