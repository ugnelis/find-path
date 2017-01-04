import tensorflow as tf
from calculations import utils
import skimage.io
import numpy as np

RESOURCE = '../../dataset'
HEIGHT = 180
WIDTH = 320
BATCH_SIZE = 2


def conv2d(x, W, b, strides=1):
    """Conv2D wrapper, with bias and relu activation."""
    x = tf.nn.conv2d(x, W, strides=[1, strides, strides, 1], padding='SAME')
    x = tf.nn.bias_add(x, b)
    return tf.nn.relu(x)


def maxpool2d(x, k=2):
    """MaxPool2D wrapper."""
    return tf.nn.max_pool(x, ksize=[1, k, k, 1], strides=[1, k, k, 1], padding='SAME')


def deconv2d(x, W, b, output_shape, strides):
    """Deconv layer"""
    deconv = tf.nn.conv2d_transpose(x, W, output_shape=output_shape, strides=strides, padding="VALID")
    deconv = tf.nn.bias_add(deconv, b)
    deconv = tf.nn.relu(deconv)
    return deconv


# Create model
def multilayer_perceptron(x, weights, biases, use_dropout=False):
    # Reshape input picture
    x = tf.reshape(x, shape=[-1, HEIGHT, WIDTH, 1])

    # Convolution Layer
    with tf.name_scope("conv1") as scope:
        conv1 = conv2d(x, weights['wc1'], biases['bc1'])
        conv1 = maxpool2d(conv1, k=2)

    # Convolution Layer
    with tf.name_scope("conv2") as scope:
        conv2 = conv2d(conv1, weights['wc2'], biases['bc2'])
        conv2 = maxpool2d(conv2, k=2)

    # Convolution Layer
    with tf.name_scope("conv3") as scope:
        conv3 = conv2d(conv2, weights['wc3'], biases['bc3'])
        conv3 = maxpool2d(conv3, k=2)

    temp_batch_size = tf.shape(x)[0]  # batch_size shape
    with tf.name_scope("deconv1") as scope:
        output_shape = [temp_batch_size, HEIGHT // 4, WIDTH // 4, 64]
        strides = [1, 2, 2, 1]
        deconv = tf.nn.conv2d_transpose(conv3, weights['wdc1'],
                                        output_shape=output_shape,
                                        strides=strides,
                                        padding="SAME")
        deconv = tf.nn.bias_add(deconv, biases['bdc1'])
        conv4 = tf.nn.relu(deconv)

    with tf.name_scope("deconv2") as scope:
        output_shape = [temp_batch_size, HEIGHT // 2, WIDTH // 2, 32]
        strides = [1, 2, 2, 1]
        conv5 = deconv2d(conv4, weights['wdc2'], biases['bdc2'], output_shape, strides)

    with tf.name_scope("deconv3") as scope:
        output_shape = [temp_batch_size, HEIGHT, WIDTH, 1]
        conv6 = tf.nn.conv2d_transpose(conv5, weights['wdc3'],
                                       output_shape=output_shape,
                                       strides=[1, 2, 2, 1],
                                       padding="VALID")
        x = tf.nn.bias_add(conv6, biases['bdc3'])

    return x


def main(argv):
    # dataset = utils.read_files(resource)
    # input, output = utils.split_dataset(dataset)

    x = tf.placeholder(tf.float32, [None, HEIGHT, WIDTH])
    y = tf.placeholder(tf.float32, [None, HEIGHT * WIDTH], name="ground_truth")

    weights = {
        # 5x5 conv, 1 input, 32 outputs
        'wc1': tf.Variable(tf.random_normal([5, 5, 1, 32])),
        # 5x5 conv, 32 inputs, 64 outputs
        'wc2': tf.Variable(tf.random_normal([5, 5, 32, 64])),
        # 5x5 conv, 32 inputs, 64 outputs
        'wc3': tf.Variable(tf.random_normal([5, 5, 64, 128])),

        'wdc1': tf.Variable(tf.random_normal([2, 2, 64, 128])),

        'wdc2': tf.Variable(tf.random_normal([2, 2, 32, 64])),

        'wdc3': tf.Variable(tf.random_normal([2, 2, 1, 32])),
    }

    biases = {
        'bc1': tf.Variable(tf.random_normal([32])),
        'bc2': tf.Variable(tf.random_normal([64])),
        'bc3': tf.Variable(tf.random_normal([128])),
        'bdc1': tf.Variable(tf.random_normal([64])),
        'bdc2': tf.Variable(tf.random_normal([32])),
        'bdc3': tf.Variable(tf.random_normal([1])),
    }

    # Construct model
    pred = multilayer_perceptron(x, weights, biases)
    pred = tf.pack(pred)
    pred = tf.reshape(pred, [-1, HEIGHT * WIDTH])

    with tf.name_scope("opt") as scope:
        cost = tf.reduce_sum(tf.pow((pred - y), 2)) / (2 * BATCH_SIZE)
        optimizer = tf.train.AdamOptimizer(learning_rate=0.001).minimize(cost)

    # Evaluate model
    with tf.name_scope("acc") as scope:
        # accuracy is the difference between prediction and ground truth matrices
        correct_pred = tf.equal(0, tf.cast(tf.sub(cost, y), tf.int32))
        accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

    # Initializing the variables
    init = tf.initialize_all_variables()

    with tf.Session() as sess:
        sess.run(init)
        # Import data
        input = [skimage.io.imread("../../dataset/1.jpg", True), skimage.io.imread("../../dataset/2.jpg", True)]
        output = [skimage.io.imread("../../dataset/1_.jpg", True), skimage.io.imread("../../dataset/2.jpg", True)]

        input = np.asarray(input)
        output = np.asarray(output)

        test_x = np.reshape(input[0], (-1, 180, 320))

        output = np.reshape(output, (2, 180 * 320))
        print(output.shape)
        for step in range(51):
            sess.run(optimizer, feed_dict={x: input, y: output})
            if step % 20 == 0:
                print("Current step: ", step)

        print("Done")
        #
        # # Make a prediction
        # prediction = sess.run(pred, feed_dict={x: test_x})
        # prediction = np.reshape(prediction, (180, 320))
        #
        # prediction[prediction > 1] = 1
        # prediction[prediction < -1] = -1
        #
        # print(prediction)
        #
        # skimage.io.imsave("works.jpg", prediction)


if __name__ == '__main__':
    tf.app.run()
