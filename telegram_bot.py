import os
import random
from time import sleep

import telegram
from dotenv import load_dotenv

import config


def generate_mixed_images() -> list:
    images: list = os.listdir(config.dir_images)
    random.shuffle(images)
    return images


if __name__ == "__main__":
    load_dotenv()

    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    message = "Мой прекрасный космос"
    seconds_in_hour = 3600
    publish_seconds_timeout: int = (
        config.telegram_hours_timeout_publish * seconds_in_hour
    )

    bot: telegram.Bot = telegram.Bot(token=os.getenv("TELEGRAM_API_TOKEN"))

    images = []

    while True:
        if not images:
            images: list = generate_mixed_images()
        image_name: str = images.pop()
        image_path: str = f"{config.dir_images}{image_name}"
        bot.send_message(text=message, chat_id=chat_id)
        with open(image_path, "rb") as image:
            bot.send_document(chat_id=chat_id, document=image)

        sleep(publish_seconds_timeout)
