import os
import random
from time import sleep

import telegram
from dotenv import load_dotenv

import config


class TelegramBot:
    def __init__(self, bot, chat_id):
        self.bot = bot
        self.chat_id = chat_id

    def get_updates(self):
        updates = self.bot.get_updates()[-1]
        print(updates)

    def send_message(self, message):
        self.bot.send_message(text=message, chat_id=self.chat_id)

    def upload_image(self, image_path: str):
        self.bot.send_document(chat_id=self.chat_id, document=open(image_path, "rb"))


def generate_mixed_images() -> list:
    images: list = os.listdir(config.dir_images)
    random.shuffle(images)
    return images


if __name__ == "__main__":
    load_dotenv()

    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    message= "Мой прекрасный космос"
    seconds_in_hour = 3600
    publish_seconds_timeout: int = (
        config.telegram_hours_timeout_publish * seconds_in_hour
    )

    bot: telegram.Bot = telegram.Bot(token=os.getenv("TELEGRAM_API_TOKEN"))
    telegram_bot: TelegramBot = TelegramBot(bot=bot, chat_id=chat_id)

    images = []

    while True:
        if not images:
            images: list = generate_mixed_images()
        image_name: str = images.pop()
        image_path: str = f'{config.dir_images}{image_name}'

        telegram_bot.send_message(message=message)
        telegram_bot.upload_image(image_path=image_path)

        sleep(publish_seconds_timeout)
