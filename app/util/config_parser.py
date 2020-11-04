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
        return self.settings['images']['folder']

    def image_formats(self):
        return self.settings['images']['formats']

    def image_files(self):
        fp = []
        for ff in self.image_formats():
            fp += glob.glob(os.path.join(self.image_folder(), '**', f'*.{ff}'), recursive=True)
        return fp

    def model(self, type):
        return self.settings['labeling'][type]['model']

    def labels(self, type):
        with open(self.settings['labeling'][type]['labels']) as f:
            data = json.load(f)
        return np.asarray(data)
