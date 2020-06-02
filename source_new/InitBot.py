import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import CallbackContext

from configparser import ConfigParser

from BaseFunction import BaseFunction
from KeywordFunction import KeywordFunction
from GroupFunction import GroupFunction
from FirebaseConnect import FirebaseConnect


import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

class TelegramBot :
    def __init__(self, token, configPath, debug=False) :
        config = ConfigParser()
        config.read(configPath, encoding="utf-8")
        self.config = config

        self.updater = Updater(token, use_context=True)
        self.dispatcher = self.updater.dispatcher

        print('Init Handlers.')
        self.initHandler(debug=debug)

        print('Booting Bot ...')
        self.updater.start_polling()
        self.updater.idle()
        

    def addCommandHandler(self, command, callback) :
        dispatcher = self.dispatcher
        handler = CommandHandler(command, callback)
        dispatcher.add_handler(handler)

    def addMessageHandler(self, callback) :
        dispatcher = self.dispatcher
        handler = MessageHandler(Filters.text & (~Filters.command), callback)
        # command를 제외한 text에만 handler 적용
        dispatcher.add_handler(handler)

    # def addErrorHandler(self, command, callback) :

    def initHandler(self, debug) :
        config = self.config
        CMD = config['CMD']
        database = FirebaseConnect(config)

        # keyword Function 불러오기
        keywordFunction = KeywordFunction(config, database)
        self.addCommandHandler(CMD['KADD'], keywordFunction.kadd)
        self.addCommandHandler(CMD['KLIST'], keywordFunction.klist)
        self.addCommandHandler(CMD['KDEL'], keywordFunction.kdel)

        # Group Function 불러오기
        groupFunction = GroupFunction(config, database)
        self.addCommandHandler(CMD['GLIST'], groupFunction.glist)

        # Base Functions
        baseFunction = BaseFunction(config, database)
        self.addCommandHandler(CMD['START'], baseFunction.start)
        self.addCommandHandler(CMD['HELP'], baseFunction.help_)
        self.addCommandHandler(CMD['HOWTO'], baseFunction.howto)

        # Debug Functions, debug=True 시에만 실행
        if debug :
            from DebugFunction import DebugFunction
            debugFunction = DebugFunction()
            
            self.addMessageHandler(debugFunction.getMessageData)
