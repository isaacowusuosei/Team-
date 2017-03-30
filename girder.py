import json
import urllib


def read_response(url):
    response = urllib.urlopen(url)

    return json.load(response)


def get_image_meta_data(image_id):
    request_url = "https://isic-archive.com:443/api/v1/image/" + image_id

    return read_response(request_url)


def get_image_id(image_name):
    request_url = "https://isic-archive.com:443/api/v1/image?limit=50&offset=0&sort=name&sortdir=1&name="

    return request_url + image_name
