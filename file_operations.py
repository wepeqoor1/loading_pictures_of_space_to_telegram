import requests


def save_image(response: requests.Response, path: str) -> None:
    with open(path, "wb") as write_file:
        write_file.write(response.content)
