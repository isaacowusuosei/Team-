import numpy as np
import argparse
import tensorflow as tf
from flask import Flask, request, jsonify

from preprocessing import inception_preprocessing
from nets import nets_factory, inception_v3


# Define all the needed global variables
image_preprocessing_fn = None
image = None
network_fn = None
eval_image_size = None
app = Flask(__name__)
checkpoint_path = None
slim = tf.contrib.slim
class_mapping = {0: 'benign', 1: 'malignant'}

@app.route('/api/classify', methods=['POST'])
def classify():
    global image_preprocessing_fn
    global network_fn
    global checkpoint_path

    with tf.Graph().as_default():
        byte_image = request.files['image'].read()

        image = tf.image.decode_jpeg(byte_image, channels=3)

        processed_image = image_preprocessing_fn(image, eval_image_size, eval_image_size)
        processed_image.set_shape((299, 299, 3))

        processed_image = tf.expand_dims(processed_image, axis=0)


        x = tf.placeholder(tf.float32, (None, 299, 299, 3))

        # Create the model, use the default arg scope to configure the batch norm parameters.
        with slim.arg_scope(inception_v3.inception_v3_arg_scope()):
            logits, _ = inception_v3.inception_v3(processed_image, num_classes=2, is_training=False)
        checkpoint_path = tf.train.latest_checkpoint(checkpoint_path)

        init_fn = slim.assign_from_checkpoint_fn(
        checkpoint_path,
        slim.get_variables_to_restore())

        probabilities = tf.nn.softmax(logits)

        with tf.Session() as sess:
            sess.run(tf.local_variables_initializer())
            init_fn(sess)

            np_image, network_input, probabilities = sess.run([image,
                                                               processed_image,
                                                               probabilities])


    predicted_label_int = np.argmax(probabilities, axis=1)
    predicted_label = class_mapping[predicted_label_int[0]]

    return jsonify(predicted_diagnosis=predicted_label)

def main():
    global image_preprocessing_fn
    global image
    global network_fn
    global eval_image_size
    global checkpoint_path

    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', type=str, default='inception_v3')
    parser.add_argument('--preprocessing_name', default=None)
    parser.add_argument('--num_classes', type=int, default=2)
    parser.add_argument('--labels_offset', type=int, default=0)
    parser.add_argument('--weight_decay', type=float, default=0.00004)
    parser.add_argument('--eval_image_size', type=str, default=None)
    parser.add_argument('--checkpoint_dir', type=str)

    args = parser.parse_args()
    image_preprocessing_fn = inception_preprocessing.preprocess_for_eval

    network_fn = nets_factory.get_network_fn(
        args.model_name,
        num_classes=(args.num_classes - args.labels_offset),
        is_training=False)

    eval_image_size = args.eval_image_size or network_fn.default_image_size

    checkpoint_path = args.checkpoint_dir

    app.run(debug=True)


if __name__ == '__main__':
    main()