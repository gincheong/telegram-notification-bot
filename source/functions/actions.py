class Actions :
    def __init__(self) :
        pass
    
    def sendAction(update, context, action) :
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
