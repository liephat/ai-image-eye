import json
import glob
import os
import numpy as np

FILE = 'config/settings.json'


class ConfigParser:

    def __init__(self):
        self.settings = None
        self.read(FILE)

    def read(self, file):
        with open(file) as f:
            self.settings = json.load(f)

    def image_files(self):
        fp = []
        for ff in self.settings['formats']:
            fp += glob.glob(os.path.join(self.image_folder(), '**', f'*.{ff}'), recursive=True)
        return fp

    def image_folder(self):
        return self.settings['image_folder']

    def model(self):
        return self.settings['model']

    def labels(self):
        with open(self.settings['labels']) as f:
            data = json.load(f)
        return np.asarray(data)
