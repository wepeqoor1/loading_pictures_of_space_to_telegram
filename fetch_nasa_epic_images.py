from pathlib import Path
from dotenv import load_dotenv

import argparse
import os
import requests
from datetime import datetime


def get_ship_launches(api_key: str) -> dict:
    """Get Earth image from NASA-API"""

    url = "https://api.nasa.gov/EPIC/api/natural/images"
    payload = {"api_key": api_key}
    response = requests.get(url, params=payload)
    response.raise_for_status()

    return response.json()


def parsing_console_arguments():
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
    nasa_api_key = os.getenv("NASA_API_KEY")

    
    dir_images = 'images'
    path_images = Path(Path.cwd(), dir_images)
    path_images.mkdir(exist_ok=True)

    args = parsing_console_arguments()
    image_count: int = args.count

    try:
        ship_launches = get_ship_launches(api_key=nasa_api_key)
    except requests.exceptions.HTTPError as http_error:
        print("Не удалось загрузить Данные о полете")
        
    for image_number, ship_launch in enumerate(ship_launches):

        if image_number >= image_count:
            break

        image, image_date = ship_launch["image"], ship_launch["date"]
        date_convert = datetime.strftime(
            datetime.fromisoformat(image_date), format="%Y/%m/%d"
        )

        image_link = f"https://api.nasa.gov/EPIC/archive/natural/{date_convert}/png/{image}.png"

        image_name = f"nasa_epic_{image_number}.png"
        
        try:
            image: requests.Response = requests.get(
                url=image_link, params={"api_key": nasa_api_key}
            )
            image.raise_for_status()
        except requests.exceptions.HTTPError as http_error:
            print("Не удалось загрузить картинку")

        with open(Path(path_images, image_name), "wb") as write_file:
            write_file.write(image.content)


