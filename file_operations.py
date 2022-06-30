import os
import requests


def check_directory(dir_name: str) -> None:
    """Checking or create directory"""
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        
        
def save_image(response: requests.Response, path: str) -> None:
    with open(path, "wb") as write_file:
        write_file.write(response)
        