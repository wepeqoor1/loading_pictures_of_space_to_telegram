import requests
import os


def download_picture(url: str, path: str) -> None:
    response = requests.get(url)
    response.raise_for_status()

    with open(path, 'wb') as write_file:
        write_file.write(response.content)


if __name__ == '__main__':

    dir_images = 'images/'
    if not os.path.exists(dir_images):
        os.makedirs(dir_images)
    
    url: str = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'
    path = ''.join([dir_images, 'hubble.jpeg'])

    try:
        download_picture(url=url, path=path)
    except requests.exceptions.HTTPError:
        print('Не удалось загрузить картинку')