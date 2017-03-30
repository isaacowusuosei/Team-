from os import listdir
from os.path import isfile, join

import argparse
import girder

def get_image_name(image_path):
    return image_path.split('/')[-1].split('.')[0]


def get_all_files(dir):
    """
    Get all files in a dir
    :param dir: path to a directory
    :return: a list of file paths in the directory
    """
    file_paths = []

    for file_path in listdir(dir):
        if isfile(join(dir, f)):
            file_paths.append(file_path)

    return file_paths

def check_dir(dir):
    """
    Checks that "/" is at the end of the dire
    :param dir: a dir
    :return: a dir with / appended if it's missing
    """
    if dir[-1] == '/':
        return dir
    else:
        return dir + '/'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', dest='path', type=str,
                        help='path where the images are located')
    parser.add_argument()

    args = parser.parse_args()

    data_path = check_dir(args.path)

    file_paths = get_all_files(data_path)

    for file_path in file_paths:
        image_name = get_image_name(file_path)
        image_id = girder.get_image_id(image_name)
        meta_data = girder.get_image_meta_data(image_id)
        meta_data.write()







if __name__ == '__main__':
    main()
