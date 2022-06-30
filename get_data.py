import requests

from file_operations import save_image


def get_image(url: str, path: str, params=None) -> None:
    response: requests.Response = requests.get(url, params=params)
    response.raise_for_status()
    save_image(response=response.content, path=path)
