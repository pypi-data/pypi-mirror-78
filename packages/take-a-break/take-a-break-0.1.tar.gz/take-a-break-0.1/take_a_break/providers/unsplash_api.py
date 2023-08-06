import shutil

import requests

from take_a_break import get_resources, jpeg_to_png
from take_a_break.providers import Provider


class UnsplashAPI(Provider):
    def __init__(self, endpoint="https://source.unsplash.com/random/1280x1080"):
        self.endpoint = endpoint

    def get_random_image(self):
        response = requests.get(self.endpoint, stream=True)
        if response.status_code == 200:
            response.raw.decode_content = True
            with open(get_resources("random.jpg"), 'wb') as f:
                shutil.copyfileobj(response.raw, f)
            return jpeg_to_png(get_resources("random.jpg"))
