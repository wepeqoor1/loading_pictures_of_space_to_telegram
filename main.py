import requests
import os
from datetime import datetime

from fetch_spacex_images import fetch_spacex_last_launch
from environment_variables import load_environment_variables
from word_processing import get_image_format
from download_and_save_image import download_and_save_image


def get_nasa_image_of_day(api_key: str, dir_images: str) -> None:
    """Get image of day from NASA-API"""

    url: str = "https://api.nasa.gov/planetary/apod/"
    payload = {"api_key": f"{api_key}", "count": 30}

    response = requests.get(url, params=payload)
    response.raise_for_status()
    response = response.json()

    for image_number, image_data in enumerate(response):
        image_link = image_data["hdurl"]
        image_format = get_image_format(url=image_link)
        image_name = f"nasa_apod_{image_number}{image_format}"

        image_path: str = "".join([dir_images, image_name])
        download_and_save_image(url=image_link, path=image_path)


def get_nasa_earth_image(api_key: str, dir_images: str, count_image: int) -> None:
    """Get image of day from NASA-API"""

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
        url_image_template = (
            f"https://api.nasa.gov/EPIC/archive/natural/{convert_date}/png/{image}.png"
        )

        image_name = f"nasa_epic_{image_number}.png"
        image_path: str = "".join([dir_images, image_name])

        download_and_save_image(url=url_image_template, path=image_path, params=payload)


def check_directory(dir_name: str) -> None:
    """Checking or create directory"""
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


if __name__ == "__main__":

    load_environment_variables()
    NASA_API_KEY = os.getenv("NASA_API_KEY")

    dir_images = "images/"
    count_nasa_earth_image = 10

    check_directory(dir_name=dir_images)

    try:
        fetch_spacex_last_launch(dir_images=dir_images)
        get_nasa_image_of_day(api_key=NASA_API_KEY, dir_images=dir_images)
        get_nasa_earth_image(
            api_key=NASA_API_KEY,
            dir_images=dir_images,
            count_image=count_nasa_earth_image,
        )
    except requests.exceptions.HTTPError:
        print("Ошибка в в получении картинки")
    else:
        print("Картинки загружены")
