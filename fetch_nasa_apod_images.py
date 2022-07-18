import argparse
import os
from pathlib import Path
from typing import Optional
from xml.dom import NotFoundErr
import requests
import urllib.parse

from dotenv import load_dotenv
from utils import download_image


def get_apod_image_of_day(api_key: str, image_count: int) -> dict:
    """Get image of day from NASA-API"""

    url = "https://api.nasa.gov/planetary/apod/"
    payload = {"api_key": api_key, "count": image_count}

    response = requests.get(url, params=payload)
    response.raise_for_status()

    return response.json()


def parsing_console_arguments():
    parser = argparse.ArgumentParser(
        description=(
            """
                Программа принимает обязательный параметр --count:
                количество случайных картинок космоса.
                """
        )
    )
    parser.add_argument(
        "count",
        help="Введите количество картинок",
        type=int,
    )

    return parser.parse_args()


def get_image_extention(url: str) -> str:
    url_with_decode_spaces = urllib.parse.unquote(url)
    path_in_url = urllib.parse.urlsplit(url_with_decode_spaces).path
    return os.path.splitext(path_in_url)[-1]


if __name__ == "__main__":
    load_dotenv()
    nasa_api_key: Optional[str] = os.getenv("NASA_API_KEY")
    if not nasa_api_key:
        raise NotFoundErr('Неправильный api ключ')

    dir_images = 'images'
    path_images = Path(Path.cwd() / dir_images)
    path_images.mkdir(exist_ok=True)

    args = parsing_console_arguments()
    image_count: int = args.count

    try:
        ship_launches = get_apod_image_of_day(
            api_key=nasa_api_key, image_count=image_count
        )

        for image_number, ship_launch in enumerate(ship_launches):
            image_link: str = ship_launch["hdurl"]
            image_extention: str = get_image_extention(url=image_link)
            image_name = f"nasa_apod_{image_number}{image_extention}"
            image_path = Path(path_images, image_name)
            download_image(url=image_link, path=image_path, params={"api_key": nasa_api_key})

    except requests.exceptions.HTTPError as http_error:
        print("Не удалось загрузить картинку")
