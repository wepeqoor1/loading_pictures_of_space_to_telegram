import requests
from pprint import pprint
import argparse

from download_and_save_image import download_and_save_image
from word_processing import get_image_format
import config
from check_directory import check_directory


def fetch_spacex_last_launch(dir_images: str, launch_id=None) -> None:
    """Get last images links from Spacex flight"""

    api_spacex_data = "https://api.spacexdata.com/v5/launches"
    response: requests.Response = requests.get(api_spacex_data)
    response.raise_for_status()
    response = response.json()
    pprint(response)

    flight_number = response[-1]["flight_number"]
    company_name: str = "spacex"

    for launch in response:
        if image_links := launch["links"]["flickr"]["original"]:
            for idx_link, image_link in enumerate(image_links):
                image_format = get_image_format(url=image_link)
                image_name: str = f"{company_name}_{idx_link}{image_format}"
                path: str = "".join([dir_images, image_name])

                download_and_save_image(url=image_link, path=path)
            break
        else:
            flight_number -= 1
            
            
def console_argument_parser():
    parser = argparse.ArgumentParser(
            description=(
                """
                Программа принимает на вход ссылки и генерирует коротки (Битлинк) ссылки.
                Так же считает количество переходов по коротким ссылкам.
                """)
            )
    parser.add_argument(
        '--id',
        help='Введите id запуска',
        )
    
    return parser.parse_args()


if __name__ == '__main__':
    check_directory(dir_name=config.dir_images)
    
    args = console_argument_parser()
    launch_id: int = args.id

    fetch_spacex_last_launch(dir_images=config.dir_images, launch_id=launch_id)