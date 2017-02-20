#!/usr/bin/env python

import os
import scipy as scp
import scipy.misc

import numpy as np
import logging
import tensorflow as tf
import sys

import fcn16_vgg
import utils

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.INFO,
                    stream=sys.stdout)

from tensorflow.python.framework import ops

img1 = scp.misc.imread("./test_data/1.jpg")
input_image = scp.misc.imread("./test_data/1.jpg")
output_image = scp.misc.imread("./test_data/1_.jpg")

with tf.Session() as sess:
    train_mode = tf.placeholder(tf.bool)
    input_placeholder = tf.placeholder("float")
    output_placeholder = tf.placeholder("float")
    batch_images = tf.expand_dims(input_placeholder, 0)

    vgg_fcn = fcn16_vgg.FCN16VGG()
    with tf.name_scope("content_vgg"):
        vgg_fcn.build(batch_images, debug=True, num_classes=2)

    print('Finished building Network.')

    logging.warning("Score weights are initialized random.")
    logging.warning("Do not expect meaningful results.")

    logging.info("Start Initializing Variabels.")

    init = tf.global_variables_initializer()
    sess.run(init)

    print('Running the Network')
    tensors = [vgg_fcn.pred, vgg_fcn.pred_up]
    down, up = sess.run(tensors, feed_dict={input_placeholder: img1, train_mode: False})

    down_color = utils.color_image(down[0])
    up_color = utils.color_image(up[0])

    scp.misc.imsave('fcn16_downsampled.png', down_color)
    scp.misc.imsave('fcn16_upsampled.png', up_color)

    print('Training the Network')
    # simple 1-step training
    cost = tf.reduce_sum((vgg_fcn.pred_up - output_image) ** 2)
    cost = tf.cast(cost, tf.float32)
    optimizer = tf.train.AdamOptimizer(0.0001)
    gradients = optimizer.compute_gradients(loss=cost)
    down, up = sess.run(gradients,
                        feed_dict={input_placeholder: input_image, output_placeholder: output_image, train_mode: True})

    scp.misc.imsave('fcn16_downsampled_1_step.png', down_color)
    scp.misc.imsave('fcn16_upsampled_1_step.png', up_color)
