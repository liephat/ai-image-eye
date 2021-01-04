import pandas as pd


class DataReader:

    def __init__(self, file):
        self.data = pd.read_csv(file)

    def get_labels(self, uid):
        return self.data.iloc[uid]['labels']

    def filelist(self):
        return self.data['file']

    def dict(self):
        return self.data.to_dict()
