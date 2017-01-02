import tensorflow as tf
from calculations import utils

resource = '../../dataset'


def main(argv):
    dataset = utils.read_files(resource)
    input, output = utils.split_dataset(dataset)


if __name__ == '__main__':
    tf.app.run()
