import requests

from download_and_save_image import download_and_save_image
from word_processing import get_image_format


def fetch_spacex_last_launch(dir_images: str) -> None:
    """Get last images links from Spacex flight"""

    api_spacex_data = "https://api.spacexdata.com/v5/launches/past"
    response: requests.Response = requests.get(api_spacex_data)
    response.raise_for_status()
    response = response.json()

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


if __name__ == '__main__':
    print()
