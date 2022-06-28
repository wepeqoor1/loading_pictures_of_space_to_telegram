from urllib import response
from dotenv import load_dotenv

import requests
import os
from pprint import pprint


def download_picture(url: str, path: str) -> None:
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
            for idx_link, picture_link in enumerate(picture_links):
                picture_name: str = f'{company_name}_{idx_link}.jpg'
                path: str = ''.join([dir_images, picture_name])
                
                download_picture(url=picture_link, path=path)
            break
        else:
            flight_number -= 1


def get_nasa_picture_of_day(api_key: str, dir_images: str) -> None:
    """Get picture of day from NASA-api"""
    
    url: str = 'https://api.nasa.gov/planetary/apod'
    payload = {
        'api_key': api_key
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()

    return response


if __name__ == '__main__':
    NASA_API_KEY = os.getenv('NASA_API_KEY')

    picture_name = 'hubble.jpeg'
    directory_images = 'images/'

    path_images: str = ''.join([directory_images, picture_name])
    url: str = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'

    """Load environment variables"""
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    if not os.path.exists(directory_images):
        os.makedirs(directory_images)
    
    try:
        fetch_spacex_last_launch(directory_images=directory_images)
        get_nasa_picture_of_day(api_key=NASA_API_KEY)
    except requests.exceptions.HTTPError:
        print('Ошибка в в получении картинки')