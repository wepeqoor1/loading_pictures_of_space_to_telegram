import os
from pathlib import Path
import requests
import argparse
import urllib.parse

from utils import download_image


def fetch_images_by_launch_id(launch_id: int) -> list:
    """Downloading images from flight number SpaceX launch"""

    url = f"https://api.spacexdata.com/v5/launches/{launch_id}"
    response: requests.Response = requests.get(url)
    
    response.raise_for_status()
    return response.json()["links"]["flickr"]["original"]


def get_image_format(url: str) -> str:
    url_with_decode_spaces = urllib.parse.unquote(url)
    path_in_url = urllib.parse.urlsplit(url_with_decode_spaces).path

    return os.path.splitext(path_in_url)[-1]


def parsing_console_arguments():
    parser = argparse.ArgumentParser(
        description=(
            """
                Программа принимает необязательный параметр (номер полета SpaceX) id
                и загружает фотографии в директорию.
                """
        )
    )
    parser.add_argument(
        "--id",
        help="Введите id запуска",
    )

    return parser.parse_args()


if __name__ == "__main__":
    dir_images = 'images'
    path_images = Path(Path.cwd(), dir_images)
    path_images.mkdir(exist_ok=True)

    args = parsing_console_arguments()
    input_launch_id = args.id
    
    launch_ids = [
        input_launch_id,
        'latest',  # last launch
        '5eb87d42ffd86e000604b384',  # Last launch with images
    ]
    
    try:
        for launch_id in launch_ids:
            if launch_id:
                image_links: list = fetch_images_by_launch_id(launch_id=launch_id)
                if image_links:
                    break
                
        for idx, image_link in enumerate(image_links):
            image_format = get_image_format(url=image_link)
            image_name: str = f"spacex_{idx}{image_format}"
            image_path = Path(path_images, image_name)
            download_image(url=image_link, path=image_path)

    except requests.exceptions.HTTPError as http_error:
        print("Данные не найдены")
