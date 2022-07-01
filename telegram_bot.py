import os
import random
import telegram

from environment_variables import load_environment_variables
import config


class TelegramBot:
    def __init__(self, bot):
        self.bot = bot
        self.chat_id = self.get_updates()

    def get_me(self):
        print(self.bot.get_me())

    def get_updates(self):
        updates = self.bot.get_updates()
        print(updates[-1])

    def send_message(self, message, chat_id):
        self.bot.send_message(text=message, chat_id=chat_id)

    def upload_picture(self, chat_id: int, image_path: str):
        self.bot.send_document(chat_id=chat_id, document=open(image_path, 'rb'))


if __name__ == "__main__":
    load_environment_variables()
    
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    message = 'Картинка дня'
    image_path = "".join(
        [config.dir_images, random.choice(os.listdir(config.dir_images))]
    )

    bot = telegram.Bot(token=os.getenv("TELEGRAM_API_TOKEN"))
    telegram_bot = TelegramBot(bot=bot)
    send_message = telegram_bot.send_message(message=message, chat_id=chat_id)
    telegram_bot.upload_picture(chat_id=chat_id, image_path=image_path)
