import numpy as np
import os.path
import glob
import json
import scipy.misc
from PIL import Image, ImageDraw
import tensorflow as tf

INPUT = 'input'
OUTPUT = 'output'

CLASSES = ['boundary', 'route', 'obstacle']


def train_test_split(input_set, output_set, test_size):
    """Split arrays or matrices into train and test subsets.

    Args:
        input_set: numpy array.
        output_set: numpy array.
        test_size: float32.
            Size of test set.

    Returns:
        train_input_set: numpy array.
        train_output_set: numpy array.
        test_input_set: numpy array.
        test_output_set: numpy array.
    """
    size = input_set.shape[0]
    test_size = int(size * test_size)
    train_input_set = input_set[:size - test_size]
    train_output_set = output_set[:size - test_size]
    test_input_set = input_set[size - test_size:size]
    test_output_set = output_set[size - test_size:size]

    return train_input_set, train_output_set, test_input_set, test_output_set


def activation_summary(x):
    """Helper to create summaries for activations.

    Creates a summary that provides a histogram of activations.
    Creates a summary that measures the sparsity of activations.

    Args:
        x: tensor.
    """
    tensor_name = x.op.name
    tf.summary.histogram(tensor_name + '/activations', x)
    tf.summary.scalar(tensor_name + '/sparsity', tf.nn.zero_fraction(x))


def read_files(dir):
    """Read files and create a dataset.

    Args:
        dir: string.
            Image directory.

    Returns:
        dataset: list of dictionaries - [{INPUT: [], OUTPUT: []}].
    """
    if not os.path.isdir(dir):
        print("Image directory '" + dir + "' not found.")
        return None

    # Allowed image types.
    extensions = ['jpg', 'jpeg']
    file_list = []

    print("Looking for images in '" + dir + "'")

    for extension in extensions:
        file_glob = os.path.join(dir, '*.' + extension)
        file_list.extend(glob.glob(file_glob))

    dataset = []

    for file in file_list:
        file_name = os.path.splitext(os.path.basename(file))[0]
        json_path = dir + '/' + file_name + '.json'

        # Check if image JSON file exists.
        if not os.path.exists(json_path):
            print("JSON file '" + json_path + "' not found.")
            continue

        # Read JSON data.
        with open(json_path) as data_file:
            data = json.load(data_file)

        input_image = scipy.misc.imread(file)

        height, width = input_image.shape[:2]

        output_image = polygons_to_regions(data['polygons'], height, width, CLASSES)
        output_image = regions_to_one_hot_encoding(output_image, len(CLASSES))

        item = {
            INPUT: input_image,
            OUTPUT: output_image
        }
        dataset.append(item)

    print("Found " + str(len(dataset)) + " images.")

    return dataset


def make_point_valid(point, height, width):
    """Make point to be in boundaries.

    Args:
        point: tuple, int32 - (x, y).
            Point which has x and y coords.
        height: int32.
            The height of the image.
        width: int32.
            The width of the image.

    Returns:
        point - tuple, int32 - (x, y).
            Point which has x and y coords.
    """
    if point[0] >= width:
        point[0] = width - 1
    elif point[0] < 0:
        point[0] = 0

    if point[1] >= height:
        point[1] = height - 1
    elif point[1] < 0:
        point[1] = 0

    return point


def polygons_to_regions(polygons, height, width, classes):
    """Make polygons as an array which different cell indicates
    different class.

    Args:
        polygons: array of dictionaries - [[{'points': [], 'type': <string>}]].
        height: int32.
            The height of the image.
        width: int32.
            The width of the image.
        classes: list, string.
            List of class labels.

    Returns:
        regions: numpy array, int32 - [height, width].
            Every cell in array is a number of the class.
    """
    # Create a zero array. Zero indicates background or boundaries.
    regions = np.zeros([height, width])

    for polygon in polygons:
        # Make points from JSON to list.
        points_list = points_to_list(polygon['points'])

        # Make points to be in boundaries.
        points_list = [make_point_valid(p, height, width) for p in points_list]

        # Make dictionary items by as tuples.
        points_list = [(x, y) for x, y in points_list]

        # Get class index.
        class_index = classes.index(polygon['type'])

        # Make an empty image and fill the polygon.
        image = Image.new('L', (width, height), 0)
        ImageDraw.Draw(image).polygon(points_list, outline=1, fill=1)

        # Set class index value to result.
        regions[np.nonzero(image)] = class_index

    return regions


def regions_to_one_hot_encoding(array, num_classes):
    """Make regions to be encoded as One Hot.

    Args:
        array: numpy array, int32 - [height, width].
            Array of the regions.
        num_classes: int32.
            The number of classes.

    Returns:
        one_hot: numpy array, int32 - [height, width, num_classes].
    """
    height, width = array.shape[:2]

    one_hot = np.zeros([height, width, num_classes])

    for i in range(height):
        for j in range(width):
            class_index = int(array[i, j])
            one_hot[i, j, class_index] = 1

    return one_hot


def one_hot_encoding_to_regions(one_hot):
    """Make One Hot to be decoded as regions.

    Args:
        one_hot: numpy array, int32 - [height, width, num_classes].
            Array of the regions.

    Returns:
        regions: numpy array, int32 - [height, width].
    """
    height, width, num_classes = one_hot.shape

    regions = np.zeros([height, width])

    for i in range(height):
        for j in range(width):
            for k in range(num_classes):
                if one_hot[i, j, k] != 0:
                    regions[i, j] = int(one_hot[i, j, k])

    return regions


def points_to_list(points):
    """Make array of dictionaries as a list.

    Args:
        points: array of dictionaries - [{'x': x_coord, 'y': y_coord}].

    Returns:
        list: points as a list.
    """
    points_list = []
    for point in points:
        points_list.append([int(point['x']), int(point['y'])])

    return points_list


def split_dataset(dataset):
    """Split dataset into input and output sets.

    Args:
        dataset: list of dictionaries - [{INPUT: [], OUTPUT: []}].

    Returns:
        input_set: numpy array.
        output_set: numpy array.
    """
    input = []
    output = []
    for data in dataset:
        input.append(data[INPUT])
        output.append(data[OUTPUT])

    return np.array(input), np.array(output)


def regions_to_colored_image(input, colors):
    """Make colored image based on region class.

    Args:
        input: numpy array, int32 - [height, width].
        colors: dictionary of colors - [num_classes].

    Returns:
        new_image: numpy array, int32 - [height, width, 3].
            Colored image.
    """
    height, width = input.shape[:2]

    new_image = np.zeros((height, width, 3))
    for i in range(len(colors)):
        new_image[input == i] = colors[i]

    return new_image


def merge_images(first_image, second_image, percentage):
    """Merge images.

    Args:
        first_image: numpy array, int32 - [height, width].
        second_image: numpy array, int32 - [height, width].
        percentage: float32.
            Percentage weight of first image.

    Returns:
        merged_image: new_image: numpy array, int32 - [height, width, 3].
    """
    merged_image = first_image * percentage + second_image * (1 - percentage)
    return merged_image
