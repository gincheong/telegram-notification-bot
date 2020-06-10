from InitBot import TelegramBot
from FirebaseConnect import FirebaseConnect

from configparser import ConfigParser # read ini files

from Logger import Logger

if __name__ == "__main__":

    CONFIG_PATH = 'config.ini'

    config = ConfigParser()
    config.read(CONFIG_PATH, encoding="utf-8")
    
    TOKEN = config['BOT']['TOKEN']

    LOGGER = Logger(config).getInstance()

    bot = TelegramBot(TOKEN, CONFIG_PATH, LOGGER)