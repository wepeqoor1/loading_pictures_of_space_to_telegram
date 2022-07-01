import os
from pprint import pprint

import telegram

from environment_variables import load_environment_variables


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


if __name__ == '__main__':
    load_environment_variables()
    
    bot = telegram.Bot(token=os.getenv('TELEGRAM_API_TOKEN'))
    telegram_bot = TelegramBot(bot=bot)
    send_message = telegram_bot.send_message('Петушок ебаный', chat_id=os.getenv('TELEGRAM_CHAT_ID'))

    