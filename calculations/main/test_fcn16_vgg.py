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


def loss(logits, labels, num_classes, head=None):
    """Calculate the loss from the logits and the labels.

    Args:
      logits: tensor, float - [batch_size, width, height, num_classes].
          Use vgg_fcn.up as logits.
      labels: Labels tensor, int32 - [batch_size, width, height, num_classes].
          The ground truth of your data.
      head: numpy array - [num_classes]
          Weighting the loss of each class
          Optional: Prioritize some classes

    Returns:
      loss: Loss tensor of type float.
    """
    with tf.name_scope('loss'):
        logits = tf.reshape(logits, (-1, num_classes))
        epsilon = tf.constant(value=1e-4)
        logits = logits
        labels = tf.to_float(tf.reshape(labels, (-1, num_classes)))

        softmax = tf.nn.softmax(logits) + epsilon

        if head is not None:
            cross_entropy = -tf.reduce_sum(tf.mul(labels * tf.log(softmax),
                                                  head), reduction_indices=[1])
        else:
            cross_entropy = -tf.reduce_sum(
                labels * tf.log(softmax), reduction_indices=[1])

        cross_entropy_mean = tf.reduce_mean(cross_entropy,
                                            name='xentropy_mean')
        tf.add_to_collection('losses', cross_entropy_mean)

        loss = tf.add_n(tf.get_collection('losses'), name='total_loss')
    return loss


img1 = scp.misc.imread("./test_data/1.jpg")

# input_image = tf.placeholder(tf.float32, shape=[None, 180, 320, 3])
# output_image = tf.placeholder(tf.int32, shape=[None, 180, 320, 1])

input_image = scp.misc.imread("./test_data/1.jpg")
output_image = scp.misc.imread("./test_data/1_.jpg", flatten=True)

#input_image = input_image.reshape((1, 180, 320, 3))
# output_image = output_image.reshape((1, 180, 320, 3)) # sita sutvarkyti ir turetu veikt


num_classes = 2

output_grounds = np.zeros([180, 320, num_classes])

# TODO fix this
for i in range(180):
    for j in range(320):
        if output_image[i, j] == 255:
            output_grounds[i, j, 0] = 1

for i in range(180):
    for j in range(320):
        if output_image[i, j] == 0:
            output_grounds[i, j, 1] = 1

print(output_grounds.shape)

with tf.device('/cpu:0'):
    with tf.Session() as sess:
        images = tf.placeholder("float")
        batch_images = tf.expand_dims(images, 0)

        input_placeholder = tf.placeholder("float")
        input_images = tf.expand_dims(input_placeholder, 0)

        output_placeholder = tf.placeholder("float")
        output_images = tf.expand_dims(output_placeholder, 0)

        true_out = tf.placeholder("float")

        train_mode = tf.placeholder(tf.bool)

        vgg_fcn = fcn16_vgg.FCN16VGG()
        with tf.name_scope("content_vgg"):
            vgg_fcn.build(batch_images, train=True, num_classes=num_classes)

        cost = loss(vgg_fcn.upscore32, true_out, num_classes)
        train = tf.train.AdamOptimizer(0.0001).minimize(cost)

        print('Finished building Network.')

        logging.warning("Score weights are initialized random.")
        logging.warning("Do not expect meaningful results.")

        logging.info("Start Initializing Variabels.")

        sess.run(tf.global_variables_initializer())

        print('Running the Network')
        tensors = [vgg_fcn.pred, vgg_fcn.pred_up]
        down, up = sess.run(tensors, feed_dict={images: img1})

        # print(vgg_fcn.upscore32.eval())
        # print (vgg_fcn.upscore32.eval())

        down_color = utils.color_image(down[0])
        up_color = utils.color_image(up[0])

        scp.misc.imsave('fcn16_downsampled.png', down_color)
        scp.misc.imsave('fcn16_upsampled.png', up_color)

        if output_grounds is None:
            print ("No values in personList")


        print('Training the Network')
        # simple 1-step training
        sess.run(train, feed_dict={images: img1, true_out: output_grounds})

        tensors = [vgg_fcn.pred, vgg_fcn.pred_up]
        down, up = sess.run(tensors, feed_dict={images: img1})
        down_color = utils.color_image(down[0])
        up_color = utils.color_image(up[0])

        scp.misc.imsave('fcn16_downsampled_1_step.png', down_color)
        scp.misc.imsave('fcn16_upsampled_1_step.png', up_color)
