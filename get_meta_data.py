import argparse
import json
import time

import girder
import utils.filesys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', dest='path', type=str,
                        help='path where the images are located')
    parser.add_argument('--output-path', dest='output_path', type=str,
                        help='path to output data to')
    args = parser.parse_args()

    data_path = utils.filesys.check_dir(args.path)
    output_path = utils.filesys.check_dir(args.output_path)
    file_paths = utils.filesys.get_all_files(data_path)

    for file_path in file_paths:
        image_name, file_extension = utils.data.get_image_name(file_path)

        if file_extension not in ('jpg', 'png'):
            continue

        image_id = girder.get_image_id(image_name)
        meta_data = girder.get_image_meta_data(image_id)

        with open(output_path + image_name + '.json', 'w+') as json_file:
            json.dump(meta_data, json_file, sort_keys=True, indent=5)
        print('Wrote {} to disk!'.format(output_path + image_name + '.json'))
        time.sleep(.6)


if __name__ == '__main__':
    main()
