import argparse
import os
import requests
from datetime import datetime
from file_operations import check_directory

from get_data import get_image
from environment_variables import load_environment_variables
import config


def get_epic_earth_image(api_key: str, count_image: int) -> None:
    """Get Earth image from NASA-API"""

    url: str = "https://api.nasa.gov/EPIC/api/natural/images"
    payload = {
        "api_key": f"{api_key}",
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    response = response.json()

    for image_number, data_image in enumerate(response):
        if image_number >= count_image:
            break

        image, date_image = data_image["image"], (data_image["date"])
        convert_date = datetime.strftime(
            datetime.fromisoformat(date_image), format="%Y/%m/%d"
        )
        url = (
            f"https://api.nasa.gov/EPIC/archive/natural/{convert_date}/png/{image}.png"
        )

        image_name = f"nasa_epic_{image_number}.png"
        image_path: str = "".join([config.dir_images, image_name])

        get_image(url=url, path=image_path, params=payload)


def console_argument_parser():
    parser = argparse.ArgumentParser(
            description=(
                """
                Программа принимает обязательный параметр --count: 
                количество картинок Земли для загрузки в директорию.
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
        get_epic_earth_image(api_key=os.getenv('NASA_API_KEY'), count_image=count_image)
    except requests.exceptions.HTTPError as http_error:
        print('Не удалось загрузить картинку')
        