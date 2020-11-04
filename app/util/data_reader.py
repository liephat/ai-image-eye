import pandas as pd

FILE = 'data.csv'


class DataReader:

    def __init__(self, file=FILE):
        self.data = pd.read_csv(file, index_col='File')

    def get_data(self, entry):
        return self.data.loc[entry]['labels']
