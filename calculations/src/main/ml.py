import numpy as np
import os.path
import glob
import re
import hashlib

resource = '../../../dataset'


def read_files_my(dir):
    if not os.path.isdir(dir):
        print("Image directory '" + dir + "' not found.")
        return None

    file_list = []

    extensions = ['jpg', 'jpeg', 'JPG', 'JPEG']

    dir_name = os.path.basename(dir)
    print("Looking for images in '" + dir_name + "'")

    for extension in extensions:
        file_glob = os.path.join(dir, '*.' + extension)
        file_list.extend(glob.glob(file_glob))

    if not file_list:
        print('No files found')

    return None


def read_files(image_dir):
    """Builds a list of training images from the file system.

    Analyzes the sub folders in the image directory, splits them into stable
    training, testing, and validation sets, and returns a data structure
    describing the lists of images for each label and their paths.

    Args:
      image_dir: String path to a folder containing subfolders of images.

    Returns:
      A dictionary containing an entry for each label subfolder,
       with images split sets within each label.
    """
    if not os.path.isdir(image_dir):
        print("Image directory '" + image_dir + "' not found.")
        return None
    result = {}
    sub_dirs = [x[0] for x in os.walk(image_dir)]
    # The root directory comes first, so skip it.
    is_root_dir = True
    for sub_dir in sub_dirs:
        if is_root_dir:
            is_root_dir = False
            continue
        extensions = ['jpg', 'jpeg', 'JPG', 'JPEG']
        file_list = []
        dir_name = os.path.basename(sub_dir)
        if dir_name == image_dir:
            continue
        print("Looking for images in '" + dir_name + "'")
        for extension in extensions:
            file_glob = os.path.join(image_dir, dir_name, '*.' + extension)
            file_list.extend(glob.glob(file_glob))
        if not file_list:
            print('No files found')
            continue
        if len(file_list) < 20:
            print('WARNING: Folder has less than 20 images, which may cause issues.')
        label_name = re.sub(r'[^a-z0-9]+', ' ', dir_name.lower())
        images = []
        for file_name in file_list:
            base_name = os.path.basename(file_name)
            images.append(base_name)

        result[label_name] = {
            'dir': dir_name,
            'set': images,
        }

    return result


def main():
    test = read_files(resource)
    print(test)

    # TODO padaryt ['tipas']['set'].len => ['visas kiekis']['dydis]['plotis']['channels']
if __name__ == '__main__':
    main()
