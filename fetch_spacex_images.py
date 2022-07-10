import os
import requests
import argparse
import urllib.parse

import config
from file_operations import check_directory, save_image


def fetch_data_by_flight_number(flight_number: int) -> dict:
    """Downloading images from flight number SpaceX launch"""

    url = f"https://api.spacexdata.com/v3/launches/{flight_number}"
    response: requests.Response = requests.get(url)
    response.raise_for_status()
    
    return response.json()


def fetch_data_by_last_launch() -> dict:
    """Downloading images from last SpaceX launch"""

    url = "https://api.spacexdata.com/v5/launches/past"
    response: requests.Response = requests.get(url)
    response.raise_for_status()
    
    return response.json()


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
    check_directory()

    args = parsing_console_arguments()
    flight_number: int = args.id

    try:
        if flight_number:
            flight: dict = fetch_data_by_flight_number(flight_number=flight_number)
            if not flight["links"]["flickr_images"] or flight.get("error"):
                raise requests.exceptions.HTTPError
            else:
                image_links = flight["links"]["flickr_images"]
        else:
            flights: dict = fetch_data_by_last_launch()
            flight_number = flights[-1]["flight_number"]
            
            for flight in flights:
                if not flight ["links"]["flickr"]["original"]:
                    flight_number -= 1
                    continue
                if image_links := flight["links"]["flickr"]["original"]:
                    break
                
        for idx, image_link in enumerate(image_links):
            image_format = get_image_format(url=image_link)
            image_name: str = f"spacex_{idx}{image_format}"
            image = requests.get(image_link)
            image.raise_for_status()
            save_image(response=image, path=f'{config.dir_images}{image_name}{image_format}')
            
    except requests.exceptions.HTTPError as er:
        print("Данные не найдены")
