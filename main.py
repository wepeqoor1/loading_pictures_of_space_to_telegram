import urllib.parse
from dotenv import load_dotenv

import requests
import os
from pprint import pprint
from datetime import date
from dateutil import parser


def download_and_save_image(url: str, path: str) -> None:
    response = requests.get(url)
    response.raise_for_status()

    with open(path, 'wb') as write_file:
        write_file.write(response.content)


def fetch_spacex_last_launch(dir_images: str) -> None:
    """Get last images links from Spacex flight"""

    api_spacex_data = 'https://api.spacexdata.com/v5/launches/past'
    response = requests.get(api_spacex_data)
    response.raise_for_status()
    response = response.json()

    flight_number = response[-1]['flight_number']
    company_name: str = 'spacex'

    for launch in response:
        if picture_links := launch['links']['flickr']['original']:
            for idx_link, image_link in enumerate(picture_links):
                image_format = get_picture_format(url=image_link)
                image_name: str = f'{company_name}_{idx_link}{image_format}'
                path: str = ''.join([dir_images, image_name])
                
                download_and_save_image(url=image_link, path=path)
            break
        else:
            flight_number -= 1


def get_nasa_image_of_day(api_key: str, dir_images: str) -> None:
    """Get picture of day from NASA-API"""
    
    url: str = 'https://api.nasa.gov/planetary/apod/'
    payload = {
        'api_key': f'{api_key}',
        'count': 30
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    response = response.json()

    for image_number, image_data in enumerate(response):
        image_link, image_format = image_data['hdurl'], get_picture_format(url=image_link)

        image_name = f'nasa_apod_{image_number}{image_format}'

        image_path: str = ''.join([dir_images, image_name])
        download_and_save_image(url=image_link, path=image_path)


def get_nasa_earth_image(api_key: str, dir_images: str) -> None:
    """Get picture of day from NASA-API"""
    
    url: str = 'https://api.nasa.gov/EPIC/api/natural/images'
    payload = {
        'api_key': f'{api_key}',
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    response = response.json()
    pprint(response)

    for image_number, data_image in enumerate(response):
        image, date_image = data_image['image'],  (data_image['date'])
        url_image = f'https://api.nasa.gov/EPIC/archive/natural/{date_image}/png/{image}.png'

        image_name = f'nasa_epic_{image_number}.png'
        image_path: str = ''.join([dir_images, image_name])

        download_and_save_image(url=url_image, path=image_path)


def get_picture_format(url: str) -> str:
    url_with_decode_spaces = urllib.parse.unquote(url)
    path_in_url = urllib.parse.urlsplit(url_with_decode_spaces).path
    return os.path.splitext(path_in_url)[-1]
    

def check_directory(dir_name: str) -> None:
    """Checking or create directory"""
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


if __name__ == '__main__':
    
    """Load environment variables"""
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    NASA_API_KEY = os.getenv('NASA_API_KEY')

    dir_images = 'images/'

    url: str = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'

    check_directory(dir_name=dir_images)
    
    try:
        # fetch_spacex_last_launch(dir_images=dir_images)
        # get_nasa_image_of_day(api_key=NASA_API_KEY, dir_images=dir_images)
        get_nasa_earth_image(api_key=NASA_API_KEY, dir_images=dir_images)
    except requests.exceptions.HTTPError:
        print('Ошибка в в получении картинки')