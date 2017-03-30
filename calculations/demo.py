# !/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import sys
import random
import datetime

import numpy as np
import scipy as scp
import scipy.misc
import tensorflow as tf

import fcn16_vgg
import utils

RESOURCE = '../dataset'
MODEL_PATH = "./models/model-250-5-10.ckpt"

# Boundary, route, obstacle.
colors = [[243, 193, 120], [0, 168, 120], [254, 94, 65]]

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.INFO,
                    stream=sys.stdout)

dataset = utils.read_files(RESOURCE)
random.shuffle(dataset)
input_set, output_set = utils.split_dataset(dataset)

height = input_set.shape[1]
width = input_set.shape[2]
num_classes = 3

input_placeholder = tf.placeholder(tf.float32, [None, height, width, num_classes])
output_placeholder = tf.placeholder(tf.float32, [None, height, width, num_classes])

vgg_fcn = fcn16_vgg.FCN16VGG('./vgg16.npy')

with tf.name_scope("content_vgg"):
    vgg_fcn.build(input_placeholder, train=True, num_classes=num_classes)

print('Finished building Network.')

# Initializing the variables.
init = tf.global_variables_initializer()

# Saver op to save and restore all the variables
saver = tf.train.Saver()

# With CPU mini-batch size can be bigger.
with tf.device('/cpu:0'):
    config = tf.ConfigProto(allow_soft_placement=True)
    config.gpu_options.allow_growth = True

    with tf.Session(config=config) as sess:
        # Restore model weights from previously saved model.
        saver.restore(sess, MODEL_PATH)

        print('Running the Network')

        prediction = sess.run(vgg_fcn.pred_up, feed_dict={input_placeholder: [input_set[0]]})

        # Original image mixed with predicted image.
        regions_image = utils.regions_to_colored_image(prediction[0], colors)
        merged_image = utils.merge_images(input_set[0], regions_image, 0.65)

        current_time = datetime.datetime.now()
        scp.misc.imsave(str(current_time) + ' prediction.png', prediction[0])
        scp.misc.imsave(str(current_time) + ' input.png', input_set[0])
        scp.misc.imsave(str(current_time) + ' output.png', output_set[0])
        scp.misc.imsave(str(current_time) + ' merged.png', merged_image)
