import tensorflow as tf
import numpy as np
import os.path
import glob
import json
from PIL import Image
import cv2

ROUTE_COLOR = (0, 153, 76)
OBSTACLE_COLOR = (128, 0, 128)
BOUNDARY_COLOR = (204, 0, 0)

INPUT = 'input'
OUTPUT = 'output'


def read_files(dir):
    if not os.path.isdir(dir):
        print("Image directory '" + dir + "' not found.")
        return None
    result = {}

    extensions = ['jpg', 'jpeg', 'JPG', 'JPEG']
    file_list = []

    print("Looking for images in '" + dir + "'")

    for extension in extensions:
        file_glob = os.path.join(dir, '*.' + extension)
        file_list.extend(glob.glob(file_glob))

    result = []
    for file in file_list:
        file_name = os.path.splitext(os.path.basename(file))[0]
        json_path = dir + '/' + file_name + '.json'

        # Check if image JSON file exists
        if not os.path.exists(json_path):
            print("JSON file '" + json_path + "' not found.")
            continue

        # Read JSON data
        with open(json_path) as data_file:
            data = json.load(data_file)

        # Create new image with regions
        image_regions_path = dir + '/' + file_name + '_.jpg'
        save_image_with_regions(file, data['polygons'])

        item = {
            INPUT: read_image(file),
            OUTPUT: read_image(image_regions_path),
            # 'data': data,
            # 'dir': file
        }
        result.append(item)

    return result


def read_image(dir):
    filename_queue = tf.train.string_input_producer([dir])
    reader = tf.WholeFileReader()
    key, value = reader.read(filename_queue)
    image = tf.image.decode_jpeg(value)
    return image


def save_image(image_tensor, image_name="image"):
    current_dir = os.getcwd()

    init = tf.initialize_all_variables()
    sess = tf.Session()
    sess.run(init)
    tf.train.start_queue_runners(sess=sess)

    img = sess.run(image_tensor)
    img = Image.fromarray(img, "RGB")
    img.save(os.path.join(current_dir, image_name + ".jpg"))


def save_image_with_regions(image_path, polygons):
    image = cv2.imread(image_path)

    image[:] = tuple(reversed(BOUNDARY_COLOR))  # Make whole image as a boundary
    for polygon in polygons:
        points_list = points_to_list(polygon['points'])
        points_list = np.array(points_list, np.int32)  # points_list needs to be numpay array
        if polygon['type'] == "route":
            cv2.fillPoly(image, [points_list], ROUTE_COLOR)

        if polygon['type'] == "obstacle":
            cv2.fillPoly(image, [points_list], OBSTACLE_COLOR)

    # Save image
    file_name = os.path.splitext(image_path)
    image_regions_path = file_name[0] + "_" + file_name[1]
    cv2.imwrite(image_regions_path, image)


def points_to_list(points):
    points_list = []
    for point in points:
        points_list.append([int(point['x']), int(point['y'])])

    return points_list


def split_dataset(dataset):
    input = []
    output = []
    for data in dataset:
        input.append(data[INPUT])
        output.append(data[OUTPUT])

    return input, output
