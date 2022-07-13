import os
import random
from time import sleep

import telegram
from dotenv import load_dotenv
from telegram.error import NetworkError


SECONDS_IN_HOUR = 3600


def generate_mixed_images(dir_images) -> list:
    images: list = os.listdir(dir_images)
    random.shuffle(images)
    return images


if __name__ == "__main__":
    load_dotenv()

    dir_images = "images/"
    hours_timeout_publish = 4
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    message = "Мой прекрасный космос"
    publish_seconds_timeout: int = hours_timeout_publish * SECONDS_IN_HOUR

    bot: telegram.Bot = telegram.Bot(token=os.getenv("TELEGRAM_API_TOKEN"))

    images = []
    timeout = 1

    while True:
        if not images:
            images: list = generate_mixed_images(dir_images=dir_images)
            image_name: str = images.pop()
            image_path: str = f"{dir_images}{image_name}"
            
        try:
            bot.send_message(text=message, chat_id=chat_id)
            with open(image_path, "rb") as image:
                bot.send_document(chat_id=chat_id, document=image)
            sleep(publish_seconds_timeout)
        except NetworkError as error:
            sleep(timeout)
            timeout = 10
            print(f'Попытка повторной отправки через {timeout} секунд')

            
        
