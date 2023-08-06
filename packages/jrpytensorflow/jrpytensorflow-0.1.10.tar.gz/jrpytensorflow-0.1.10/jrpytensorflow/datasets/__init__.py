from sklearn.datasets import make_circles
from tensorflow import keras
import pkg_resources
import pandas as pd


def load_circles():
    return make_circles(200, random_state=1, noise=0.05)


def load_fashion_mnist():
    fashion_mnist = keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

    train_images = train_images / 255.0
    test_images = test_images / 255.0

    labels = {
        k: v for k, v in zip(
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            [
                'tshirt', 'trouser', 'pullover', 'dress', 'coat',
                'sandal', 'shirt', 'sneaker', 'bag', 'boot'
            ]
        )
    }

    return train_images, train_labels, test_images, test_labels, labels


def load_walking():
    resource_path = '/'.join(('data', 'walking.zip'))
    return pd.read_csv(pkg_resources.resource_filename(
        __name__, resource_path
    ))
