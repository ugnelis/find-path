#!/usr/bin/env python

import logging
import sys

import numpy as np
import scipy as scp
import scipy.misc
import tensorflow as tf

import fcn16_vgg
import loss
import utils

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.INFO,
                    stream=sys.stdout)



img1 = scp.misc.imread("./test_data/1.jpg")
img2 = scp.misc.imread("./test_data/2.jpg")

# input_image = tf.placeholder(tf.float32, shape=[None, 180, 320, 3])
# output_image = tf.placeholder(tf.int32, shape=[None, 180, 320, 1])

input_image = scp.misc.imread("./test_data/1.jpg")
output_image = scp.misc.imread("./test_data/1_.jpg", flatten=True)

# input_image = input_image.reshape((1, 180, 320, 3))
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

        cost = loss.loss(vgg_fcn.upscore32, true_out, num_classes)
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
        for i in range(15):
            # simple 1-step training
            sess.run(train, feed_dict={images: img1, true_out: output_grounds})

        tensors = [vgg_fcn.pred, vgg_fcn.pred_up]
        down, up = sess.run(tensors, feed_dict={images: img2})
        down_color = utils.color_image(down[0])
        up_color = utils.color_image(up[0])

        scp.misc.imsave('fcn16_downsampled_50_step.png', down_color)
        scp.misc.imsave('fcn16_upsampled_50_step.png', up_color)
