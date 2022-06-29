import urllib.parse
import os


def get_image_format(url: str) -> str:
    url_with_decode_spaces = urllib.parse.unquote(url)
    path_in_url = urllib.parse.urlsplit(url_with_decode_spaces).path
    return os.path.splitext(path_in_url)[-1]