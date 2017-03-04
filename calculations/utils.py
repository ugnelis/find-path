import numpy as np
import os.path
import glob
import json
import cv2
import scipy as scp
import scipy.misc
from PIL import Image, ImageDraw
import tensorflow as tf

ROUTE_COLOR = (0, 0, 0)
OBSTACLE_COLOR = (128, 0, 128)
BOUNDARY_COLOR = (255, 255, 255)

INPUT = 'input'
OUTPUT = 'output'

CLASSES = ['boundary', 'route', 'obstacle']


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
    extensions = ['jpg', 'jpeg', 'JPG', 'JPEG']
    file_list = []

    print("Looking for images in '" + dir + "'")

    for extension in extensions:
        file_glob = os.path.join(dir, '*.' + extension)
        file_list.extend(glob.glob(file_glob))

    dataset = []

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

        input_image = scipy.misc.imread(file)

        height, width = input_image.shape[:2]

        output_image = polygons_to_regions(data['polygons'], height, width, CLASSES)
        output_image = regions_to_one_hot_encoding(output_image, len(CLASSES))

        item = {
            INPUT: input_image,
            OUTPUT: output_image
        }
        dataset.append(item)

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


def save_polygons_to_regions_image(image_path, polygons):
    """Save polygons as an image with regions.

    Args:
        image_path: string.
        polygons: array of dictionaries - [[{'points': [], 'type': <string>}]].
    """
    image = cv2.imread(image_path)

    # Make whole image as a boundary
    image[:] = tuple(reversed(BOUNDARY_COLOR))

    for polygon in polygons:
        points_list = points_to_list(polygon['points'])

        # points_list needs to be Numpy array
        points_list = np.array(points_list, np.int32)

        if polygon['type'] == "route":
            cv2.fillPoly(image, [points_list], ROUTE_COLOR)

        if polygon['type'] == "obstacle":
            cv2.fillPoly(image, [points_list], OBSTACLE_COLOR)

    # Save image
    file_name = os.path.splitext(image_path)
    image_regions_path = file_name[0] + "_" + file_name[1]
    cv2.imwrite(image_regions_path, image)


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


def color_image(image, num_classes=20):
    import matplotlib as mpl
    import matplotlib.cm
    norm = mpl.colors.Normalize(vmin=0., vmax=num_classes)
    mycm = mpl.cm.get_cmap('Set1')
    return mycm(norm(image))
