import os
import random
from time import sleep
from pathlib import Path

import telegram
from dotenv import load_dotenv
from telegram.error import NetworkError


SECONDS_IN_HOUR = 3600


def generate_mixed_images(path_images) -> list:
    images: list = os.listdir(path_images)
    random.shuffle(images)
    return images


if __name__ == "__main__":
    load_dotenv()

    dir_images = 'images'
    path_images = Path(Path.cwd(), dir_images)
    
    hours_timeout_publish = 4
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    message = "Мой прекрасный космос"
    publish_seconds_timeout: int = hours_timeout_publish * SECONDS_IN_HOUR
    
    telegram_api_token = os.getenv("TELEGRAM_API_TOKEN")
    bot: telegram.Bot = telegram.Bot(token=telegram_api_token)

    images = []
    timeout = 1

    while True:
        if not images:
            images: list = generate_mixed_images(path_images=path_images)
            image_name: str = images.pop()
            
        try:
            with open(Path(path_images, image_name), "rb") as image:
                bot.send_document(chat_id=chat_id, document=image, caption=message)
            sleep(publish_seconds_timeout)
        except NetworkError:
            sleep(timeout)
            timeout = 10
            print(f'Попытка повторной отправки через {timeout} секунд')

            
        
