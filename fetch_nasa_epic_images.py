from dotenv import load_dotenv

import argparse
import os
import requests
from datetime import datetime

from file_operations import check_directory, save_image
import config


def get_ship_launches(payload: str) -> dict:
    """Get Earth image from NASA-API"""

    url = "https://api.nasa.gov/EPIC/api/natural/images"

    response = requests.get(url, params=payload)
    response.raise_for_status()

    return response.json()


def parsing_console_argument():
    parser = argparse.ArgumentParser(
        description=(
            """
                Программа принимает обязательный параметр --count: 
                количество картинок Земли для загрузки в директорию.
                """
        )
    )
    parser.add_argument(
        "count",
        help="Введите количество картинок",
        type=int,
    )

    return parser.parse_args()


if __name__ == "__main__":
    load_dotenv()
    check_directory()

    args = parsing_console_argument()
    image_count: int = args.count

    payload = {"api_key": os.getenv("NASA_API_KEY")}

    try:
        ship_launches = get_ship_launches(payload=payload)

        for image_number, ship_launch in enumerate(ship_launches):

            if image_number >= image_count:
                break

            image, image_date = ship_launch["image"], ship_launch["date"]
            date_convert = datetime.strftime(
                datetime.fromisoformat(image_date), format="%Y/%m/%d"
            )

            image_link = f"https://api.nasa.gov/EPIC/archive/natural/{date_convert}/png/{image}.png"

            image_name = f"nasa_epic_{image_number}.png"
            image_path = f"{config.dir_images}{image_name}"

            image: requests.Response = requests.get(
                url=image_link, params={"api_key": os.getenv("NASA_API_KEY")}
            )
            image.raise_for_status()

            save_image(response=image, path=image_path)

    except requests.exceptions.HTTPError as http_error:
        print("Не удалось загрузить картинку")
