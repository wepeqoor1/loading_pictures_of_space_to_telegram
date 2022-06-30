import argparse
import os
import requests
from file_operations import check_directory

from get_data import get_image
from environment_variables import load_environment_variables
from word_processing import get_image_format
import config


def get_apod_image_of_day(api_key: str, count_image: int) -> None:
    """Get image of day from NASA-API"""

    url: str = "https://api.nasa.gov/planetary/apod/"
    payload = {
        "api_key": f"{api_key}", 
        "count": count_image
        }

    response = requests.get(url, params=payload)
    response.raise_for_status()
    response = response.json()

    for image_number, image_data in enumerate(response):
        image_link = image_data["hdurl"]
        image_format = get_image_format(url=image_link)
        image_name = f"nasa_apod_{image_number}{image_format}"

        image_path: str = "".join([config.dir_images, image_name])
        get_image(url=image_link, path=image_path)


def console_argument_parser():
    parser = argparse.ArgumentParser(
            description=(
                """
                Программа принимает обязательный параметр --count: 
                количество случайных картинок дня.
                """)
            )
    parser.add_argument(
        'count', 
        help='Введите количество картинок',
        type=int,
        )
    
    return parser.parse_args()


if __name__ == '__main__':
    load_environment_variables()
    check_directory()
    
    args = console_argument_parser()
    count_image: int = args.count
    
    try:
        get_apod_image_of_day(api_key=os.getenv('NASA_API_KEY'), count_image=count_image)
    except requests.exceptions.HTTPError as http_error:
        print('Не удалось загрузить картинку')
