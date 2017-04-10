#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import os
import sys

import numpy as np
import scipy as scp
import scipy.misc
import scipy.ndimage
import tensorflow as tf

import fcn16_vgg
import loss
import utils

RESOURCE = '../dataset'

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.INFO,
                    stream=sys.stdout)

input_set = np.load('input_set.npy')
output_set = np.load('output_set.npy')

input_set = input_set[:1]
output_set = output_set[:1]

train_input_set, train_output_set, test_input_set, test_output_set \
    = utils.train_test_split(input_set, output_set, 0.1)

train_input_set, train_output_set, valid_input_set, valid_output_set \
    = utils.train_test_split(train_input_set, train_output_set, 0.1)

height = input_set.shape[1]
width = input_set.shape[2]
num_classes = 3

epochs = 3
batch_size = 1
size = input_set.shape[0]
num_steps = epochs * size // batch_size
output_at_step = 25


def save(filters, scale_times=1, name='layer', directory='out'):
    """Save particular layer filters into images.

    Args:
        filters: numpy array.
            Filters array.
        scale_times: int32.
            Scale image times.
        name: string.
            Layer name.
        directory: string.
            Directory path, in this path image will be saved.
    """
    # Create directory if not exists.
    if not os.path.exists(directory):
        os.makedirs(directory)

    filters_num = filters.shape[3]

    for i in range(filters_num):
        image = filters[0:, :, :, i]
        height = image.shape[1]
        width = image.shape[2]
        image = image.reshape((height, width))
        image = np.resize(image, (height, width))

        rgb_image = np.zeros((height, width, 3), dtype=np.uint8)
        rgb_image[:, :, 0] = image - fcn16_vgg.VGG_MEAN[2]
        rgb_image[:, :, 1] = image - fcn16_vgg.VGG_MEAN[1]
        rgb_image[:, :, 2] = image - fcn16_vgg.VGG_MEAN[0]
        rgb_image = scipy.misc.imresize(rgb_image, (height * scale_times, width * scale_times))
        scp.misc.imsave(directory + "/" + name + "-filter-" + str(i) + ".jpg", rgb_image)


with tf.device('/cpu:0'):
    config = tf.ConfigProto(allow_soft_placement=True)
    config.gpu_options.allow_growth = True

    with tf.Session(config=config) as sess:

        input_placeholder = tf.placeholder(tf.float32, [None, height, width, num_classes])
        output_placeholder = tf.placeholder(tf.float32, [None, height, width, num_classes])

        vgg_fcn = fcn16_vgg.FCN16VGG('./vgg16.npy')

        with tf.name_scope('content_vgg'):
            vgg_fcn.build(input_placeholder, train=True, num_classes=num_classes, debug=True)

        with tf.name_scope('loss'):
            loss = loss.loss(vgg_fcn.upscore32, output_placeholder, num_classes)
            optimizer = tf.train.AdamOptimizer(0.0001).minimize(loss)

        print('Finished building Network.')

        # Initializing the variables.
        init = tf.global_variables_initializer()

        # Run initialized variables.
        sess.run(init)

        print('Running the Network')
        print('Training the Network')
        for step in range(num_steps):
            offset = (step * batch_size) % size
            batch_input = input_set[offset:(offset + batch_size), :]
            batch_output = output_set[offset:(offset + batch_size), :]

            _, l, conv1_1 = sess.run([optimizer, loss, vgg_fcn.conv1_1],
                                     feed_dict={input_placeholder: batch_input,
                                                output_placeholder: batch_output})

            # Output intermediate step information.
            if (step + 1) % output_at_step == 0:
                save(conv1_1, name='conv1_1'+str(step))
                break
