import base64
import argparse
import tensorflow as tf

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image-path', type=str)
    args = parser.parse_args()

    image_data = tf.gfile.FastGFile(args.image_path, 'r').read()

if __name__ == '__main__':
    main()