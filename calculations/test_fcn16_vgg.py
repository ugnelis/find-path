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

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.INFO,
                    stream=sys.stdout)

dataset = utils.read_files(RESOURCE)
input_set, output_set = utils.split_dataset(dataset)

test_image = input_set[-1]

height = input_set.shape[1]
width = input_set.shape[2]
num_classes = 3

epochs = 2
batch_size = 5
size = input_set.shape[0]
num_steps = epochs * size // batch_size


# TODO make cross validation.
# TODO prediction output at step.
# TODO model graph saving.
# TODO code for TensorBoard.

def result(sess):
    tensors = [vgg_fcn.pred, vgg_fcn.pred_up]
    down, up = sess.run(tensors, feed_dict={input_placeholder: [test_image]})
    down_color = utils.color_image(down[0], num_classes)
    up_color = utils.color_image(up[0], num_classes)

    scp.misc.imsave('fcn16_downsampled.png', down_color)
    scp.misc.imsave('fcn16_upsampled.png', up_color)


config = tf.ConfigProto(allow_soft_placement=True)
config.gpu_options.allow_growth = True
with tf.Session(config=config) as sess:
    input_placeholder = tf.placeholder(tf.float32, [None, height, width, num_classes])
    output_placeholder = tf.placeholder(tf.float32, [None, height, width, num_classes])

    vgg_fcn = fcn16_vgg.FCN16VGG()
    with tf.name_scope("content_vgg"):
        vgg_fcn.build(input_placeholder, train=True, num_classes=num_classes)

    loss = loss.loss(vgg_fcn.upscore32, output_placeholder, num_classes)
    optimizer = tf.train.AdamOptimizer(0.0001).minimize(loss)

    print('Finished building Network.')

    logging.warning("Score weights are initialized random.")
    logging.warning("Do not expect meaningful results.")

    logging.info("Start Initializing Variabels.")

    sess.run(tf.global_variables_initializer())

    print('Running the Network')
    print('Training the Network')
    for step in range(num_steps):
        offset = (step * batch_size) % size
        batch_input = input_set[offset:(offset + batch_size), :]
        batch_output = output_set[offset:(offset + batch_size), :]

        _, l = sess.run([optimizer, loss],
                        feed_dict={input_placeholder: batch_input, output_placeholder: batch_output})
        if step % 2 == 0:
            print("Minibatch loss at step %d: %f" % (step, l))
            # TODO make prediction output at step.

    result(sess)
