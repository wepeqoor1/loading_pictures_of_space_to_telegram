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
    company_name = 'spacex'

    for launch in response:
        if picture_links := launch['links']['flickr']['original']:
            for idx_link, picture_link in enumerate(picture_links):
                picture_name: str = f'{company_name}_{idx_link}.jpg'
                path = ''.join([dir_images, picture_name])
                
                download_picture(url=picture_link, path=path)
            break
        else:
            flight_number -= 1


if __name__ == '__main__':

    picture_name = 'hubble.jpeg'
    dir_images = 'images/'

    if not os.path.exists(dir_images):
        os.makedirs(dir_images)
    
    path_images: str = ''.join([dir_images, picture_name])
    url: str = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'

    try:
        fetch_spacex_last_launch(dir_images=dir_images)
    except requests.exceptions.HTTPError:
        print('Ошибка в в получении картинки')