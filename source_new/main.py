from InitBot import TelegramBot
from FirebaseConnect import FirebaseConnect

from configparser import ConfigParser # read ini files

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

if __name__ == "__main__":

    CONFIG_PATH = 'config.ini'

    config = ConfigParser()
    config.read(CONFIG_PATH, encoding="utf-8")
    TOKEN = config['BOT']['TOKEN']

    bot = TelegramBot(TOKEN, CONFIG_PATH)