import tensorflow as tf
from calculations import utils

resource = '../../dataset'


def main():
    test = utils.read_files(resource)
    print(test)


if __name__ == '__main__':
    main()
