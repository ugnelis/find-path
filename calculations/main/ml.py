import tensorflow as tf
from calculations import utils
import skimage.io

resource = '../../dataset'


def conv2d(x, W, b, strides=1):
    """Conv2D wrapper, with bias and relu activation."""
    x = tf.nn.conv2d(x, W, strides=[1, strides, strides, 1], padding='SAME')
    x = tf.nn.bias_add(x, b)
    return tf.nn.relu(x)


def maxpool2d(x, k=2):
    """MaxPool2D wrapper."""
    return tf.nn.max_pool(x, ksize=[1, k, k, 1], strides=[1, k, k, 1], padding='SAME')


def deconv2d(prev_layer, w, b, output_shape, strides):
    """Deconv layer"""
    deconv = tf.nn.conv2d_transpose(prev_layer, w, output_shape=output_shape, strides=strides, padding="VALID")
    deconv = tf.nn.bias_add(deconv, b)
    deconv = tf.nn.relu(deconv)
    return deconv


def main(argv):
    # dataset = utils.read_files(resource)
    # input, output = utils.split_dataset(dataset)
    input = skimage.io.imread("../../dataset/1.jpg")
    output = skimage.io.imread("../../dataset/1_.jpg")

    # Initializing the variables
    init = tf.initialize_all_variables()

    with tf.Session() as sess:
        sess.run(init)


if __name__ == '__main__':
    tf.app.run()
