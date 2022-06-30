from xml.dom import NotFoundErr
import requests
import argparse

import config
from get_data import get_image
from word_processing import get_image_format
from file_operations import check_directory


def fetch_images_flight_number(dir_images: str, flight_number: int):
    """Downloading images from flight number SpaceX launch"""
    
    url = f'https://api.spacexdata.com/v3/launches/{flight_number}'
    response: requests.Response = requests.get(url)
    response.raise_for_status()
    response: dict = response.json()
    
    if not (image_links := response["links"]["flickr_images"]) or response.get('error'):
        return NotFoundErr
    
    iterate_over_links(image_links=image_links, dir_images=dir_images)


def fetch_images_last_launch(dir_images: str, flight_number=None) -> None:
    """Downloading images from last SpaceX launch"""
        
    url = "https://api.spacexdata.com/v5/launches/past"
    response: requests.Response = requests.get(url)
    response.raise_for_status()
    response = response.json()

    flight_number = response[-1]["flight_number"]

    for launch in response:
        if image_links := launch["links"]["flickr"]["original"]:
            iterate_over_links(image_links, dir_images)
            break
        else:
            flight_number -= 1
    
    
def iterate_over_links(image_links: list, dir_images: str):
    for idx_link, image_link in enumerate(image_links):
                image_format = get_image_format(url=image_link)
                image_name: str = f"spacex_{idx_link}{image_format}"
                get_image(url=image_link, path="".join([dir_images, image_name]))
    

def console_argument_parser():
    parser = argparse.ArgumentParser(
            description=(
                """
                Программа принимает необязательный параметр (номер полета SpaceX) id
                и загружает фотографии в директорию.
                """)
            )
    parser.add_argument('--id', help='Введите id запуска',)
    
    return parser.parse_args()


if __name__ == '__main__':
    check_directory(config.dir_images)
    
    args = console_argument_parser()
    flight_number: int = args.id
        
    try:
        if flight_number: 
            fetch_images_flight_number(
                dir_images=config.dir_images,
                flight_number=flight_number
                )
            print(f'Фотографии с запуска ракеты №{flight_number} скачены')
        else:
            fetch_images_last_launch(config.dir_images)
            print('Фотографии с последнего запуска ракеты скачены')
    except requests.exceptions.HTTPError as er:
        print('Данные не найдены')
    else:
        print('Картинки загружены')