import tensorflow as tf
import numpy as np
import os.path
import glob
import json
from PIL import Image

resource = '../../../dataset'


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

        with open(json_path) as data_file:
            data = json.load(data_file)

        item = {
            'image': read_image(file),
            'data': data
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


def main():
    test = read_files(resource)
    print(test)


if __name__ == '__main__':
    main()
