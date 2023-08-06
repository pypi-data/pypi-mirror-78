from sklearn.datasets import make_circles
import pandas as pd
import pkg_resources
import torchvision
import numpy as np


def load_circles():
    return make_circles(200, random_state=1, noise=0.05)


def load_walking():
    resource_path = '/'.join(('data', 'walking.zip'))
    return pd.read_csv(pkg_resources.resource_filename(
        __name__, resource_path
    ))


def load_fashion_mnist(root, download):
    trainset = torchvision.datasets.FashionMNIST(
        root, train=True, download=download
    )
    testset = torchvision.datasets.FashionMNIST(
        root, train=False, download=download
    )
    print('Preparing array data')
    X_train = np.vstack([np.array(x).flatten() for x, _ in trainset])
    y_train = np.array([y.item() for _, y in trainset]).reshape(-1)
    X_test = np.vstack([np.array(x).flatten() for x, _ in testset])
    y_test = np.array([y.item() for _, y in testset]).reshape(-1, 1)
    labels = {k: v for k, v in zip(
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [
            'tshirt', 'trouser', 'pullover', 'dress', 'coat',
            'sandal', 'shirt', 'sneaker', 'bag', 'boot'
        ]
    )}
    print('Done!')
    return X_train, X_test, y_train, y_test, labels
