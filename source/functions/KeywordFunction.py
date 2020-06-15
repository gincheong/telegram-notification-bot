from datetime import datetime
from configparser import ConfigParser

class KeywordFunction :
    def __init__(self, config, database, logger) :
        self.database = database
        self.logger = logger
        
        self.URL = config['URL']
        self.KEY = config['KEY']
        self.CMD = config['CMD']

    def getFullName(self, update) :
        firstName = update.message.from_user.first_name
        try :
            lastName = update.message.from_user.last_name
            fullName = " ".join([lastName, firstName])
        except :
            fullName = firstName
        
        return fullName
        
    def parseCommandInput(self, command, text) :
        if text == ('/' + command) :
            return ""
        else :
            commandInput = text[len(command) + 2 : ]
            commandInput = commandInput.strip().lower() # 좌우 공백 제거, 소문자 변환
            return commandInput

    def kadd(self, update, context) :
        if update.effective_chat.type == "private" :
            database = self.database

            CMD = self.CMD

            senderId = update.effective_chat.id
            senderMessage = update.message.text
            commandInput = self.parseCommandInput(CMD['KADD'], senderMessage)

            if commandInput == "" :
                message = (
                    "추가할 키워드를 명령어와 함께 입력해주세요." "\n"
                    "예시) /" + CMD['KADD'] + " 예나" "\n"
                    "(\"예나\" 키워드를 추가)" 
                )
                self.logger.info("kadd Help : uid:{}".format(senderId))
            else :
                storedKeywords = database.getKeywordDict(senderId)

                # 키워드 초기 등록이거나, 새로운 키워드 등록인 경우
                if commandInput not in storedKeywords.values() :
                    
                    database.addKeywordToUser(commandInput, senderId)
                    
                    message = (
                        commandInput + " 키워드를 추가했습니다."
                    )
                    self.logger.info("kadd Success : uid:{}, keyword:{}".format(senderId, commandInput))
                else : # 중복 키워드를 등록하려는 경우
                    message = (
                        "이미 등록된 키워드입니다."
                    )
                    self.logger.info("kadd Duplicated : uid:{}, keyword:{}".format(senderId, commandInput))
            
            context.bot.send_message(chat_id=senderId, text=message)

            
    def klist(self, update, context) :
        if update.effective_chat.type == "private" :
            database = self.database
            
            senderId = update.effective_chat.id
            
            storedKeywords = database.getKeywordDict(senderId)

            if len(storedKeywords) == 0 :
                message = (
                    "등록된 키워드가 없습니다."
                )
                self.logger.info("klist NoData : uid:{}".format(senderId))
            else :
                message = (
                    "등록된 키워드 목록입니다." "\n" + 
                    ", ".join(storedKeywords.values())
                )
                self.logger.info("klist Success : uid:{}".format(senderId))
            context.bot.send_message(chat_id=senderId, text=message)

    def kdel(self, update, context) :
        if update.effective_chat.type == "private" :
            database = self.database

            CMD = self.CMD

            senderId = update.effective_chat.id
            senderMessage = update.message.text
            commandInput = self.parseCommandInput(CMD['KDEL'], senderMessage)

            if commandInput == "" :
                message = (
                    "삭제할 키워드를 명령어와 함께 입력해주세요." "\n"
                    "예시) /" + CMD['KDEL'] + " 예나" "\n"
                    "(\"예나\" 키워드를 삭제)" 
                )
                self.logger.info("kdel Help : uid:{}".format(senderId))
            else :
                storedKeywords = database.getKeywordDict(senderId)

                # 삭제 실패
                if len(storedKeywords) == 0 :
                    message = (
                        "등록된 키워드가 없습니다."
                    )
                    self.logger.info("kdel NoData : uid:{}, keyword:{}".format(senderId, commandInput))
                elif commandInput not in storedKeywords.values() :
                    message = (
                        "등록되지 않은 키워드입니다."
                    )
                    self.logger.info("kdel NoKeyword : uid:{}, keyword:{}".format(senderId, commandInput))
                else :
                    for key, val in storedKeywords.items() :
                        if val == commandInput :
                            database.deleteKeyword(key, senderId)
                            break
                    message = (
                        commandInput + " 키워드를 삭제했습니다."
                    )
                    self.logger.info("kdel Success : uid:{}, keyword:{}".format(senderId, commandInput))
                
            context.bot.send_message(chat_id=senderId, text=message)

    # 키워드 대조하는 함수, MessageHandler에 추가되어 매 채팅마다 실행됨
    def isKeywordUsed(self, update, context) :
        # 키워드 알림은 그룹 채팅에서만 작동합니다
        if update.effective_chat.type == 'group' :
            database = self.database
            currentHour = datetime.today().hour

            URL = self.URL

            senderId = update.message.from_user.id
            senderMessage = update.message.text
            senderName = self.getFullName(update)
            messageId = update.message.message_id
            groupId = update.effective_chat.id
            groupName = update.effective_chat.title

            # 그룹에 있는 사용자를 먼저 조회하기
            storedGroupUsers = database.get(URL['GROUP'] + '/' + str(groupId) + URL['USER'])
            if storedGroupUsers == None :
                # 등록된 사용자가 없으면 함수 종료
                return
            
            # 그룹에 등록된 각 사용자의 키워드 정보를 확인하기
            for user in storedGroupUsers.values() :
                
                # 1. 본인의 대화에는 키워드 감지를 하지 않음
                if user == str(senderId) :
                    continue

                # 2. 방해금지 시간대가 설정되었는지 확인함
                start, end = database.getDoNotDisturb(user)
                if start == "off" or start == None :
                    pass
                else :
                    start, end = int(start), int(end)
                    if self.isInHour(start, end, currentHour) :
                        continue

                # 3. 키워드를 확인함
                keywords = database.getKeywordDict(user).values()

                usedKeyword = self.isKeywordInMessage(keywords, senderMessage)
                if usedKeyword == False :
                    pass
                else :
                    message = (
                        "{} 님이 호출했습니다.".format(senderName) + "\n"
                        "그룹 이름 : {}".format(groupName) + "\n"
                        "메세지 내용 : {}".format(senderMessage)
                    )

                    # 알림 메세지 사용자에게 전송
                    context.bot.send_message(chat_id=user, text=message, disable_web_page_preview=True)
                    self.logger.info("Notifications : uid:{}, gid:{}, mid:{}".format(user, groupId, messageId))

            
    def isKeywordInMessage(self, keywords, message) :
        # 키워드가 메시지에 있는지 확인
        
        message = message.lower() # 대소문자를 구분하지 않음
        for keyword in keywords :
            if keyword in message :
                # 키워드가 발견되면, 발견된 키워드를 반환
                return keyword
        # 발견된 키워드 없으면 False 반환        
        return False

    def isInHour(self, start, end, currentHour) :
        
        if start == end : # 같은 시간을 입력함
            return False # 알람을 끈 것으로 간주함

        if start == 0 :
            if currentHour < end :
                return True
            else :
                return False
        
        if end == 0 :
            if currentHour >= start : 
                return True
            else :
                return False
            
        if start < end :
            if currentHour >= start and currentHour < end :
                return True
            else :
                return False
        else : # start > end
            if currentHour >= start and currentHour <= 23 \
                or \
               currentHour >= 0 and currentHour < end :
                return True
            else :
                return False
