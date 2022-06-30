import os

def check_directory(dir_name: str) -> None:
    """Checking or create directory"""
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)