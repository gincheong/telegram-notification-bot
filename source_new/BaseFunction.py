import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

class BaseFunction :
    def __init__(self) :
        pass

    def start(self, update, context) :
        if update.effective_chat.type == "private" :
            senderId = update.effective_chat.id
            message = (
                "내가 등록한 키워드가 그룹 채팅방에서 사용되면, 봇이 메시지를 전송합니다." "\n"
                "/howto 명령어로 사용방법을 확인하세요."
            )
            context.bot.send_message(chat_id=senderId, text=message, parse_mode="html")

        elif update.effective_chat.type == "group" :
            senderId = update.message.from_user.id
            messageId = update.message.message_id
            
            # Firebase 연결
            if "그룹이 이미 등록된 경우" :
                message = (
                    "이미 등록된 그룹입니다." "\n"
                    "기타 명령어는 봇과의 개인 대화에서만 작동합니다."
                )
            elif "그룹을 새로 등록하는 경우" :
                message = (
                    "현재 그룹을 키워드 알림 봇에 등록합니다." "\n"
                    "기타 명령어는 봇과의 개인 대화에서만 작동합니다."
                )
            
            context.bot.send_message(chat_id=senderId, text=message, reply_to_message_id=messageId)


    def help_(self, update, context) :
        if update.effective_chat.type == "private" :
            # only available in private chat
            senderId = update.effective_chat.id
            message = (
                "/kadd <i>[keyword]</i> : 알람을 받을 키워드를 추가합니다." "\n"
                "/kdel <i>[keyword]</i> : 등록된 키워드를 삭제합니다."
            )
            context.bot.send_message(chat_id=senderId, text=message, parse_mode="html")

    def howto(self, update, context) :
        if update.effective_chat.type == "private" :
            # only available in private chat
            senderId = update.effective_chat.id
            message = (
                "1. 키워드 알림을 활성화할 그룹 채팅에 봇을 초대합니다." "\n"
                "2. <b>그룹 내 채팅으로</b> /start@keywordNoti_Bot 을 입력합니다." "\n"
                "3. <b>봇과의 개인 대화로</b> 키워드를 등록합니다." "\n"
                "다른 명령어는 /help 명령어로 확인할 수 있습니다."
            )
            context.bot.send_message(chat_id=senderId, text=message, parse_mode="html")