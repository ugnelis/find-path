import tensorflow as tf
from calculations import utils
import skimage.io
import numpy as np

RESOURCE = '../../dataset'
HEIGHT = 180
WIDTH = 320


# Create model
def multilayer_perceptron(x, weights, biases, use_dropout=False):
    # Reshape input picture
    x = tf.reshape(x, shape=[-1, HEIGHT, WIDTH, 1])
    batch_size = tf.shape(x)[0]

    # 1st convolution layer
    with tf.name_scope("conv1") as scope:
        conv1 = tf.nn.conv2d(x, weights['wc1'], strides=[1, 1, 1, 1], padding='SAME')
        conv1 = tf.nn.bias_add(conv1, biases['bc1'])
        conv1 = tf.nn.relu(conv1)
        conv1 = tf.nn.max_pool(conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

    # 2nd convolution layer
    with tf.name_scope("conv2") as scope:
        conv2 = tf.nn.conv2d(conv1, weights['wc2'], strides=[1, 1, 1, 1], padding='SAME')
        conv2 = tf.nn.bias_add(conv2, biases['bc2'])
        conv2 = tf.nn.relu(conv2)
        conv2 = tf.nn.max_pool(conv2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

    # 3rd convolution layer
    with tf.name_scope("conv3") as scope:
        conv3 = tf.nn.conv2d(conv2, weights['wc3'], strides=[1, 1, 1, 1], padding='SAME')
        conv3 = tf.nn.bias_add(conv3, biases['bc3'])
        conv3 = tf.nn.relu(conv3)
        conv3 = tf.nn.max_pool(conv3, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

    # 1st deconvolution layer
    with tf.name_scope("deconv1") as scope:
        output_shape = [batch_size, HEIGHT // 4, WIDTH // 4, 64]
        deconv1 = tf.nn.conv2d_transpose(conv3,
                                         weights['wdc1'],
                                         output_shape=output_shape,
                                         strides=[1, 2, 2, 1],
                                         padding="SAME")
        deconv1 = tf.nn.bias_add(deconv1, biases['bdc1'])
        deconv1 = tf.nn.relu(deconv1)

    # 2nd deconvolution layer
    with tf.name_scope("deconv2") as scope:
        output_shape = [batch_size, HEIGHT // 2, WIDTH // 2, 32]
        deconv2 = tf.nn.conv2d_transpose(deconv1,
                                         weights['wdc2'],
                                         output_shape=output_shape,
                                         strides=[1, 2, 2, 1],
                                         padding="VALID")
        deconv2 = tf.nn.bias_add(deconv2, biases['bdc2'])
        deconv2 = tf.nn.relu(deconv2)

    # 3rd deconvolution layer
    with tf.name_scope("deconv3") as scope:
        output_shape = [batch_size, HEIGHT, WIDTH, 1]
        deconv3 = tf.nn.conv2d_transpose(deconv2,
                                         weights['wdc3'],
                                         output_shape=output_shape,
                                         strides=[1, 2, 2, 1],
                                         padding="VALID")
        deconv3 = tf.nn.bias_add(deconv3, biases['bdc3'])

    return deconv3


def main(argv):
    # Import data
    dataset = utils.read_files_with_skimage(RESOURCE)
    input, output = utils.split_dataset(dataset)
    batch_size = len(input)

    # Make data as Numpy array
    input = np.asarray(input)
    output = np.asarray(output)

    # HEIGHT * WIDTH because y place holder also has HEIGHT * WIDTH
    output = np.reshape(output, (batch_size, HEIGHT, WIDTH))

    # Test value
    test_x = skimage.io.imread("../../dataset/1.jpg", True)
    test_x = np.reshape(test_x, (1, 180, 320))

    # Tensorflow placeholders
    x = tf.placeholder(tf.float32, [None, HEIGHT, WIDTH])
    y = tf.placeholder(tf.float32, [None, HEIGHT, WIDTH], name="ground_truth")

    weights = {
        # 5x5 conv, 1 input, 32 outputs
        'wc1': tf.Variable(tf.random_normal([3, 3, 1, 32])),
        # 5x5 conv, 32 inputs, 64 outputs
        'wc2': tf.Variable(tf.random_normal([3, 3, 32, 64])),
        'wc3': tf.Variable(tf.random_normal([3, 3, 64, 128])),
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
    pred = tf.reshape(pred, [-1, HEIGHT,  WIDTH])

    with tf.name_scope("opt") as scope:
        cost = tf.reduce_sum(tf.pow((pred - y), 2)) / (2 * batch_size)
        optimizer = tf.train.AdamOptimizer(learning_rate=0.01).minimize(cost)

    # Evaluate model
    with tf.name_scope("acc") as scope:
        # accuracy is the difference between prediction and ground truth matrices
        correct_pred = tf.equal(0, tf.cast(tf.sub(cost, y), tf.int32))
        accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

    # Initializing the variables
    init = tf.global_variables_initializer()

    with tf.Session() as sess:
        sess.run(init)

        # Initializing summary writer for TensorBoard
        train_writer = tf.summary.FileWriter ('/tmp/log_dir/', sess.graph)

        for step in range(10):
            feed_dict = {x: input, y: output}
            _, loss, acc = sess.run([optimizer, cost, accuracy], feed_dict=feed_dict)

            if step % 10 == 0:
                print("Minibatch loss at step ", step, ": ", cost)
                print("Minibatch accuracy: ", acc)

        print("Done")

        # Make a prediction
        prediction = sess.run(pred, feed_dict={x: test_x})
        prediction = np.reshape(prediction, (HEIGHT, WIDTH))
        prediction = prediction.astype(int)
        print(prediction)

        prediction[prediction > 255] = 255
        prediction[prediction < 0] = 0

        print(prediction)

        skimage.io.imsave("works.jpg", prediction)


if __name__ == '__main__':
    tf.app.run()
