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
        fp = self.settings['labeling'][_type]['labels']
        fe = os.path.splitext(fp)[1].lower()

        with open(fp, 'r') as f:
            if fe == '.json':
                data = json.load(f)
                names = np.asarray(data)
            else:
                names = np.asarray([name.strip('\n') for name in f.readlines()])

        return names

    def anchors_file(self, _type):
        return self.settings['labeling'][_type]['anchors']

    def data_file(self):
        return self.settings['data']['file']
