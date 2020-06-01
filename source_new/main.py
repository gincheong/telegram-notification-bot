from InitBot import TelegramBot

from configparser import ConfigParser # read ini files

if __name__ == "__main__":

    config = ConfigParser()
    config.read('config.ini')
    
    TOKEN = config['BOT']['TOKEN']
    FIREBASE_URL = config['FIREBASE']['URL']
    FIREBASE_CERTPATH = config['FIREBASE']['CERTPATH']

    bot = TelegramBot(TOKEN, debug=True)