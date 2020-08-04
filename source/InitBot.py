import traceback
import telegram
from telegram import Update, error
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import CallbackContext

from configparser import ConfigParser

from Functions import Functions
from FirebaseConnect import FirebaseConnect

from Logger import Logger

class TelegramBot :
    def __init__(self, token, configPath, logger) :
        self.logger = logger

        config = ConfigParser()
        config.read(configPath, encoding="utf-8")
        self.config = config

        self.updater = Updater(token, use_context=True)
        self.dispatcher = self.updater.dispatcher

        print('Init Handlers')
        logger.info("Init Handlers")
        self.initHandler()

        print('Booting Bot ...')
        logger.info("Booting Bot ...")
        
        self.updater.start_polling()
        self.updater.idle()
        logger.info("Bot Exited ...")
        

    def addCommandHandler(self, command, callback) :
        dispatcher = self.dispatcher
        handler = CommandHandler(command, callback)
        dispatcher.add_handler(handler)

    def addMessageHandler(self, callback) :
        dispatcher = self.dispatcher
        handler = MessageHandler(Filters.text & (~Filters.command) & (~Filters.update.edited_message), callback)
        # command를 제외한 text에만 handler 적용
        dispatcher.add_handler(handler)

    def addMigrateHandler(self, callback) :
        dispatcher = self.dispatcher
        handler = MessageHandler(Filters.status_update.migrate, callback)
        dispatcher.add_handler(handler)

    def addLeftChatMemberHandler(self, callback) :
        dispatcher = self.dispatcher
        handler = MessageHandler(Filters.status_update.left_chat_member, callback)
        dispatcher.add_handler(handler)

    def addNewChatTitleHandler(self, callback) :
        dispatcher = self.dispatcher
        handler = MessageHandler(Filters.status_update.new_chat_title, callback)
        dispatcher.add_handler(handler)

    def errorHandler(self, update, context) :
        adminId = self.config['ADMIN']['ID']

        try :
            raise context.error
        except Exception :
            self.logger.error(update.effective_chat) # 어차피 gid, mid 등으로 메세지 트래킹은 할 수 없긴 함
            self.logger.error(update.message.from_user)

            errorLog = traceback.format_exc()
            self.logger.error(errorLog)
            context.bot.send_message(chat_id=adminId, text=errorLog, disable_notification=True)
            # 에러 발생하면 나한테 전송함
        except error.BadRequest :
            self.logger.error(update.effective_chat)
            self.logger.error(update.message.from_user)
            
            errorLog = traceback.format_exc()
            self.logger.error(errorLog)
            context.bot.send_message(chat_id=adminId, text="BadRequest 에러 발생함", disable_notification=True)

    def initHandler(self) :
        logger = self.logger
        config = self.config
        CMD = config['CMD']
        database = FirebaseConnect(config)
        functions = Functions(config, database, logger)

        # keyword Function 불러오기
        keywordFunction = functions.keyword
        self.addCommandHandler(CMD['KADD'], keywordFunction.kadd)
        self.addCommandHandler(CMD['KDEL'], keywordFunction.kdel)
        self.addCommandHandler(CMD['KLIST'], keywordFunction.klist)
        self.addMessageHandler(keywordFunction.isKeywordUsed)

        # Group Function 불러오기
        groupFunction = functions.group
        self.addCommandHandler(CMD['GLIST'], groupFunction.glist)

        # Base Functions 불러오기
        baseFunction = functions.base
        self.addCommandHandler(CMD['START'], baseFunction.start)
        self.addCommandHandler(CMD['HELP'], baseFunction.help_)
        self.addCommandHandler(CMD['HOWTO'], baseFunction.howto)
        self.addCommandHandler(CMD['DELETE'], baseFunction.delete)
        self.addCommandHandler(CMD['STOP'], baseFunction.stop)
        self.addCommandHandler(CMD['DONOTDISTURB'], baseFunction.doNotDisturb)
        
        self.addLeftChatMemberHandler(baseFunction.leftChatMember)
        self.addNewChatTitleHandler(baseFunction.newChatTitle)

        self.addMigrateHandler(baseFunction.detectMigrate)

        # Error Handler
        self.dispatcher.add_error_handler(self.errorHandler)