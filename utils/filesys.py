import os


def get_all_files(dir):
    """
    Get all files recursively in a dir
    :param dir: path to a directory
    :return: a list of file paths in the directory
    """
    file_paths = []

    for dp, dn, filenames in os.walk(dir):
        for f in filenames:
            file_paths.append(os.path.join(dp, f))

    return file_paths


def check_dir(dir):
    """
    Just checks that "/" is at the end of the directory path
    :param dir: a dir
    :return: a dir with / appended if it's missing
    """
    if dir[-1] == '/':
        return dir
    else:
        return dir + '/'

def get_image_name(image_path):
    return image_path.split('/')[-1].split('.')
