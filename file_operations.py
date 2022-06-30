from distutils.command.config import config
import os
import requests

import config

def check_directory() -> None:
    """Checking or create directory"""
    if not os.path.exists(config.dir_images):
        os.makedirs(config.dir_images)
        
        
def save_image(response: requests.Response, path: str) -> None:
    with open(path, "wb") as write_file:
        write_file.write(response)
        