from configparser import ConfigParser

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

class KeywordFunction :
    def __init__(self, config, database) :
        self.database = database
        
        self.URL = config['URL']
        self.KEY = config['KEY']
        self.CMD = config['CMD']

    def getFullname(self, update) :
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

            URL = self.URL
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
            else :
                storedKeywords = database.get(URL['USER'] + '/' + str(senderId) + URL['KEYWORD'])

                if (storedKeywords == None or # 키워드 초기 등록이거나
                    commandInput not in storedKeywords.values()) : # 새 키워드인 경우
                    
                    database.push(URL['USER'] + '/' + str(senderId) + URL['KEYWORD'], commandInput)
                    
                    message = (
                        commandInput + " 키워드를 추가했습니다."
                    )
                else : # 중복 키워드를 등록하려는 경우
                    message = (
                        "이미 등록된 키워드입니다."
                    )
            
            context.bot.send_message(chat_id=senderId, text=message)

            
    def klist(self, update, context) :
        if update.effective_chat.type == "private" :
            database = self.database
            
            URL = self.URL

            senderId = update.effective_chat.id
            
            storedKeywords = database.get(URL['USER'] + '/' + str(senderId) + URL['KEYWORD'])

            if storedKeywords == None :
                message = (
                    "등록된 키워드가 없습니다."
                )
            else :
                message = (
                    "등록된 키워드 목록입니다." "\n" + 
                    ", ".join(storedKeywords.values())
                )
            context.bot.send_message(chat_id=senderId, text=message)

    def kdel(self, update, context) :
        if update.effective_chat.type == "private" :
            database = self.database

            URL = self.URL
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
            else :
                storedKeywords = database.get(URL['USER'] + '/' + str(senderId) + URL['KEYWORD'])

                # 삭제 실패
                if storedKeywords == None :
                    message = (
                        "등록된 키워드가 없습니다."
                    )
                elif commandInput not in storedKeywords.values() :
                    message = (
                        "등록되지 않은 키워드입니다."
                    )
                else :
                    for key, val in storedKeywords.items() :
                        if val == commandInput :
                            database.delete(URL['USER'] + '/' + str(senderId) + URL['KEYWORD'] + '/' + key)
                            break
                    message = (
                        commandInput + " 키워드를 삭제했습니다."
                    )
                
            context.bot.send_message(chat_id=senderId, text=message)