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

RESOURCE = '../dataset'


def main(argv):
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                        level=logging.INFO,
                        stream=sys.stdout)

    dataset = utils.read_files(RESOURCE)
    input_set, output_set = utils.split_dataset(dataset)

    input_set = input_set[0]
    output_set = output_set[0]

    img1 = scp.misc.imread("./test_data/1.jpg")
    img2 = scp.misc.imread("./test_data/2.jpg")

    input_image = scp.misc.imread("./test_data/1.jpg")
    output_image = scp.misc.imread("./test_data/1_.jpg", flatten=True)

    num_classes = 3

    with tf.device('/cpu:0'):
        with tf.Session() as sess:

            input_placeholder = tf.placeholder("float")
            input_images = tf.expand_dims(input_placeholder, 0)

            output_placeholder = tf.placeholder("float")
            output_images = tf.expand_dims(output_placeholder, 0)


            vgg_fcn = fcn16_vgg.FCN16VGG()
            with tf.name_scope("content_vgg"):
                vgg_fcn.build(input_images, train=True, num_classes=num_classes)

            cost = loss.loss(vgg_fcn.upscore32, output_placeholder, num_classes)
            train = tf.train.AdamOptimizer(0.0001).minimize(cost)

            print('Finished building Network.')

            logging.warning("Score weights are initialized random.")
            logging.warning("Do not expect meaningful results.")

            logging.info("Start Initializing Variabels.")

            sess.run(tf.global_variables_initializer())

            print('Running the Network')
            tensors = [vgg_fcn.pred, vgg_fcn.pred_up]
            down, up = sess.run(tensors, feed_dict={input_placeholder: img1})


            down_color = utils.color_image(down[0])
            up_color = utils.color_image(up[0])

            scp.misc.imsave('fcn16_downsampled.png', down_color)
            scp.misc.imsave('fcn16_upsampled.png', up_color)

            print('Training the Network')
            for i in range(10):
                sess.run(train, feed_dict={input_placeholder: input_set, output_placeholder: output_set})

            tensors = [vgg_fcn.pred, vgg_fcn.pred_up]
            down, up = sess.run(tensors, feed_dict={input_placeholder: img2})
            down_color = utils.color_image(down[0], num_classes)
            up_color = utils.color_image(up[0], num_classes)

            scp.misc.imsave('fcn16_downsampled_50_step.png', down_color)
            scp.misc.imsave('fcn16_upsampled_50_step.png', up_color)


if __name__ == '__main__':
    tf.app.run()

