import requests


def download_image(url: str, path: str, params=None) -> None:
    response: requests.Response = requests.get(url, params=params)
    response.raise_for_status()
    with open(path, "wb") as write_file:
        write_file.write(response.content)
