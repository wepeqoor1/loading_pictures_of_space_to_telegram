import argparse
import os
import requests
import urllib.parse

from dotenv import load_dotenv

from file_operations import check_directory, save_image
import config


def get_apod_image_of_day(api_key: str, count_image: int) -> None:
    """Get image of day from NASA-API"""

    url = "https://api.nasa.gov/planetary/apod/"
    payload = {"api_key": api_key, "count": count_image}

    response = requests.get(url, params=payload)
    response.raise_for_status()

    return response.json()


def parsing_console_argument():
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
    check_directory()

    args = parsing_console_argument()
    count_image: int = args.count

    try:
        ship_launches = get_apod_image_of_day(
            api_key=os.getenv("NASA_API_KEY"), count_image=count_image
        )

        for image_number, ship_launch in enumerate(ship_launches):
            image_link: str = ship_launch["hdurl"]
            image_extention: str = get_image_extention(url=image_link)
            image_name = f"nasa_apod_{image_number}{image_extention}"
            image_path = f"{config.dir_images}{image_name}"

            image: requests.Response = requests.get(
                url=image_link, params={"api_key": os.getenv("NASA_API_KEY")}
            )
            image.raise_for_status()

            save_image(response=image, path=image_path)

    except requests.exceptions.HTTPError as http_error:
        print("Не удалось загрузить картинку")
