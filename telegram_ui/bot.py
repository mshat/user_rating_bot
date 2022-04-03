import os
import telebot
from dotenv import dotenv_values

BASEDIR = os.path.abspath(os.path.dirname(__file__))
config = dotenv_values(os.path.join(BASEDIR, '.env'))
TG_TOKEN = config['TG_TOKEN']


class TgBot:
    bot = telebot.TeleBot(TG_TOKEN)

    def __init__(self):
        @self.bot.message_handler()
        def get_text_messages(message):
            print(f'NEW MESSAGE {message}')

    def _prepare_message(self, msg: str):
        msg = msg.replace('\n', ' ')
        msg = msg.replace('  ', ' ')
        return msg


def run_bot():
    tg_bot = TgBot()
    tg_bot.bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    run_bot()


