from telegram import error
import sys

class Actions :
    def __init__(self) :
        pass
    
    def sendAction(update, context, action) :
        try :
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
        except error.Unauthorized :
            self.logger.error("error occured: {}".format(sys._getframe().f_code.co_name))
            self.logger.error("telegram.error.Unauthorized: uid:{}, {}".format(user, error.Unauthorized.message))