""" numpy dataset"""

from .dataset import Dataset

class NumpyDataset(Dataset):
    def __init__(self, X, Y, transform=None):
        """
        :param X: input
        :param Y: target/labels
        :param transform: preprocess function.
        """
        self.X = X
        self.Y = Y
        assert len(self.X) == len(self.Y), "size of X and Y is not equal!"
        self.transform = transform

    def __getitem__(self, index):
        return self.get_sample(index)

    def __len__(self):
        return len(self.X)

    def get_sample(self, index):
        x = self.X[index]
        y = self.Y[index]

        data = {"x": x, "y": y}
        # if self.transform:
        #     data = self.transform(data)

        return data
