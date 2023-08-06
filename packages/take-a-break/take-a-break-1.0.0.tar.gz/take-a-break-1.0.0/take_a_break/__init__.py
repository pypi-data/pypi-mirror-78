__version__ = "1.0.0"

import os

import requests
from PIL import Image


def get_resources(filename):
    """
    :param filename: the name of the filname
    :return: the filename path from resources folder
    """
    dirname = os.path.join(os.path.dirname(__file__), 'resources')
    fullname = os.path.join(dirname, filename)
    return fullname


def temp_file(filename):
    """
    :param filename:
    :return: the filename path from the TEMP folder
    """
    pass


def get_random_joke():
    response = requests.get("http://api.icndb.com/jokes/random")
    if response.status_code == requests.codes.ok:
        joke = response.json()["value"]["joke"]
        print(joke)
        joke = joke.replace("&quot;", "\"")
        return joke
    else:
        return "Take a brake! You need it!"


def jpeg_to_png(image):
    png_image = "{}.png".format(os.path.splitext(image)[0])
    Image.open(image).save(png_image)
    os.remove(image)
    return png_image
