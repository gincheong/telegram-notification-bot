import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import CallbackContext

from BaseFunction import BaseFunction

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

class TelegramBot :
    def __init__(self, token, debug=False) :
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
        handler = MessageHandler(Filters.text & (~Filters.command), callback) # command를 제외한 text에만 handler 적용
        dispatcher.add_handler(handler)

    # def addErrorHandler(self, command, callback) :

    def initHandler(self, debug) :

        # keyword Function 불러오기


        # Group Function 불러오기


        # Base Functions
        baseFunction = BaseFunction()
        self.addCommandHandler('start', baseFunction.start)
        self.addCommandHandler('help', baseFunction.help_)
        self.addCommandHandler('howto', baseFunction.howto)

        # Debug Functions, debug=True 시에만 실행
        if debug :
            from DebugFunction import DebugFunction
            debugFunction = DebugFunction()
            
            self.addMessageHandler(debugFunction.getMessageData)
