#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import sys
import random

import numpy as np
import scipy as scp
import scipy.misc
import tensorflow as tf

import fcn16_vgg
import loss
import utils

RESOURCE = '../dataset'
MODEL_PATH = "./models/model.ckpt"

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.INFO,
                    stream=sys.stdout)

dataset = utils.read_files(RESOURCE)
random.shuffle(dataset)
input_set, output_set = utils.split_dataset(dataset)

train_input_set, train_output_set, test_input_set, test_output_set \
    = utils.train_test_split(input_set, output_set, 0.1)

train_input_set, train_output_set, valid_input_set, valid_output_set \
    = utils.train_test_split(train_input_set, train_output_set, 0.1)

height = input_set.shape[1]
width = input_set.shape[2]
num_classes = 3

epochs = 10
batch_size = 5
size = train_input_set.shape[0]
num_steps = epochs * size // batch_size


def compare(predicted_data, real_data):
    """Compare predicted image with real image.

    Args:
        predicted_data: numpy array, int32 - [height, width].
            Array of the prediction.
        real_data: numpy array, int32 - [height, width].
            Array of the real.

    Returns:
        result: float32.
            Similarity of the images.
    """
    num_equals = 0
    height, width = predicted_data.shape[:2]

    for i in range(height):
        for j in range(width):
            if predicted_data[i, j] == real_data[i, j]:
                num_equals += 1

    result = 100.0 * num_equals / (height * width)
    return result


def accuracy(predicted_batch_set, real_batch_set):
    """Get accuracy of predicted data.

    Args:
        predicted_batch_set: numpy array, int32 - [batch_size, width, height].
            The predicted data.
        real_batch_set: numpy array, int32 - [batch_size, width, height].
            The ground truth of the data.

    Returns:
        Accuracy of predicted data.
    """
    predicted_batch_size = predicted_batch_set.shape[0]
    real_batch_size = real_batch_set.shape[0]

    assert (predicted_batch_size == real_batch_size)

    sum = 0.0
    for i in range(predicted_batch_size):
        sum += compare(predicted_batch_set[i], real_batch_set[i])

    return sum / predicted_batch_size


# With CPU mini-batch size can be bigger.
with tf.device('/cpu:0'):
    config = tf.ConfigProto(allow_soft_placement=True)
    config.gpu_options.allow_growth = True

    with tf.Session(config=config) as sess:
        input_placeholder = tf.placeholder(tf.float32, [None, height, width, num_classes])
        output_placeholder = tf.placeholder(tf.float32, [None, height, width, num_classes])

        vgg_fcn = fcn16_vgg.FCN16VGG('./vgg16.npy')

        with tf.name_scope("content_vgg"):
            vgg_fcn.build(input_placeholder, train=True, num_classes=num_classes)

        with tf.name_scope("loss"):
            loss = loss.loss(vgg_fcn.upscore32, output_placeholder, num_classes)
            optimizer = tf.train.AdamOptimizer(0.0001).minimize(loss)
            tf.summary.scalar("loss", loss)

        print('Finished building Network.')

        # Initializing the variables.
        init = tf.global_variables_initializer()

        # Saver op to save and restore all the variables.
        saver = tf.train.Saver()

        # Merge all the summaries and write them out.
        merged_summary_op = tf.summary.merge_all()

        # Initializing summary writer for TensorBoard.
        summary_writer = tf.summary.FileWriter('./log_dir/work', tf.get_default_graph())

        # Run initialized variables.
        sess.run(init)

        print('Running the Network')
        print('Training the Network')
        for step in range(num_steps):
            offset = (step * batch_size) % size
            batch_input = train_input_set[offset:(offset + batch_size), :]
            batch_output = train_output_set[offset:(offset + batch_size), :]

            _, l, predictions, summary = sess.run([optimizer, loss, vgg_fcn.pred_up, merged_summary_op],
                                                  feed_dict={input_placeholder: batch_input,
                                                             output_placeholder: batch_output})

            # Write logs at every iteration.
            summary_writer.add_summary(summary, epochs * offset + step)

            # Output intermediate step information.
            if (step + 1) % 25 == 0:
                print("Minibatch loss at step %d: %f" % (step + 1, l))
                print("Minibatch accuracy: %.1f%%" % accuracy(predictions, batch_output.argmax(axis=3)))

                valid_prediction = sess.run(vgg_fcn.pred_up, feed_dict={input_placeholder: valid_input_set})
                print("Validation accuracy: %.1f%%" % accuracy(valid_prediction, valid_output_set.argmax(axis=3)))

        # Get accuracy of the test set.
        test_prediction = sess.run(vgg_fcn.pred_up, feed_dict={input_placeholder: test_input_set})
        print("Test accuracy: %.1f%%" % accuracy(test_prediction, test_output_set.argmax(axis=3)))

        # Save model weights to disk.
        save_path = saver.save(sess, MODEL_PATH)
        print("Model saved in file: %s" % save_path)
