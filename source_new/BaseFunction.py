from configparser import ConfigParser

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

class BaseFunction :
    def __init__(self, config, database) :
        self.database = database
        
        self.URL = config['URL']
        self.KEY = config['KEY']
        self.CMD = config['CMD']

    def start(self, update, context) :
        # Private Chat
        if update.effective_chat.type == "private" :
            senderId = update.effective_chat.id
            message = (
                "내가 등록한 키워드가 그룹 채팅방에서 사용되면, 봇이 메시지를 전송합니다." "\n"
                "/howto 명령어로 사용방법을 확인하세요."
            )
            context.bot.send_message(chat_id=senderId, text=message)

        # Group Chat
        elif update.effective_chat.type == "group" :
            database = self.database
            
            URL = self.URL
            KEY = self.KEY

            senderId = update.message.from_user.id
            messageId = update.message.message_id

            groupId = update.effective_chat.id
            groupName = update.effective_chat.title

            # Firebase 연결

            ''' GROUP 쪽 데이터 작업 '''
            # 그룹 신규 등록 or 그룹 이름 최신화
            database.update(URL['GROUP'] + '/' + str(groupId) + URL['INFO'],
                { KEY['GROUPNAME'] : groupName }
            )
            # Todo#3
            storedGroupUsers = database.get(URL['GROUP'] + '/' + str(groupId) + URL['USER']) # GROUP쪽에 등록된 사용자 목록
            if storedGroupUsers == None :
                storedGroupUsers = {}

            if str(senderId) not in storedGroupUsers.values() :
                # 신규 등록
                database.push(URL['GROUP'] + '/' + str(groupId) + URL['USER'], str(senderId))
            else :
                pass

            ''' USER 쪽 데이터 '''
            storedRegisteredGroups = database.get(URL['USER'] + '/' + str(senderId) + URL['REGISTERED_GROUP']) # USER쪽에 등록된 그룹 목록
            if storedRegisteredGroups == None :
                storedRegisteredGroups = {}

            if str(groupId) not in storedRegisteredGroups.keys() :
                # 신규 등록
                database.update(URL['USER'] + '/' + str(senderId) + URL['REGISTERED_GROUP'],
                    { str(groupId) : True }
                )
                message = (
                    "현재 그룹을 키워드 알림 봇에 등록합니다." "\n"
                    "기타 명령어는 봇과의 개인 대화에서만 작동합니다."
                )
            else :
                message = (
                    "이미 등록된 그룹입니다." "\n"
                    "기타 명령어는 봇과의 개인 대화에서만 작동합니다."
                )

            context.bot.send_message(chat_id=groupId, text=message, reply_to_message_id=messageId)
            

    def delete(self, update, context) :
        if update.effective_chat.type == "private" :
            senderId = update.effective_chat.id
            message = (
                "등록 해제를 원하는 그룹 채팅방에서 명령어를 입력해주세요."
            )
            context.bot.send_message(chat_id=senderId, text=message)

        elif update.effective_chat.type == "group" :
            database = self.database
        
            CMD = self.CMD
            URL = self.URL

            senderId = update.message.from_user.id
            messageId = update.message.message_id

            groupId = update.effective_chat.id

            ''' GROUP쪽 데이터 삭제 '''
            # Todo#3
            storedGroupUsers = database.get(URL['GROUP'] + '/' + str(groupId) + URL['USER'])
            if storedGroupUsers == None :
                storedGroupUsers = {} # None 반환되어 아래 조건문 에러나는것 방지

            if str(senderId) not in storedGroupUsers.values() :
                pass
            else : 
                for key, val in storedGroupUsers.items() :
                    if val == str(senderId) :
                        database.delete(URL['GROUP'] + '/' + str(groupId) + URL['USER'] + '/' + key)
                        break

            ''' USER쪽 데이터 삭제 '''
            storedRegisteredGroups = database.get(URL['USER'] + '/' + str(senderId) + URL['REGISTERED_GROUP'])
            if storedRegisteredGroups == None :
                storedRegisteredGroups = {}
            
            if str(groupId) not in storedRegisteredGroups.keys() :
                message = (
                    "등록되지 않은 그룹입니다."
                )
            else :
                database.delete(URL['USER'] + '/' + str(senderId) + URL['REGISTERED_GROUP'] + '/' + str(groupId))
                message = (
                    "현재 그룹 등록을 해제했습니다." "\n"
                    "/" + CMD['START'] + " 명령어로 다시 등록할 수 있습니다."
                )
        
            context.bot.send_message(chat_id=groupId, text=message, reply_to_message_id=messageId)
            # 메세지는 USER쪽 데이터 기준으로 전송, 어차피 항상 같이 동작하니 큰 문제는 없을듯...

    def stop(self, update, context) :
        if update.effective_chat.type == "private" :
            database = self.database
        
            CMD = self.CMD
            URL = self.URL

            senderId = update.effective_chat.id
            senderMessage = update.message.text

            
            if senderMessage == ("/" + CMD['STOP'] + " ALL") :
                # registered_group 통해서, GROUP 쪽에 등록된 사용자 아이디 모두 지우기
                ''' GROUP쪽 데이터 삭제 '''
                storedRegisteredGroups = database.get(URL['USER'] + '/' + str(senderId) + URL['REGISTERED_GROUP'])

                if storedRegisteredGroups == None :
                    pass
                else :
                    # 비효율의 끝..?
                    for eachGroupId, val in storedRegisteredGroups.items() :
                        # USER에 저장된 groupId를 가지고, GROUP쪽을 돌면서 삭제함
                        storedGroupUsers = database.get(URL['GROUP'] + '/' + str(eachGroupId) + URL['USER'])
                        if storedGroupUsers == None :
                            storedGroupUsers = {}

                        if str(senderId) not in storedGroupUsers.values() :
                            pass
                        else :
                            for key, val in storedGroupUsers.items() :
                                if val == str(senderId) :
                                    database.delete(URL['GROUP'] + '/' + str(eachGroupId) + URL['USER'] + '/' + key)
                                    break

                ''' USER쪽 데이터 삭제 '''
                database.delete(URL['USER'] + '/' + str(senderId))
                message = (
                    "사용자 정보를 모두 삭제헀습니다." "\n"
                    "/" + CMD['START'] + " 명령어로 언제든 봇을 다시 이용할 수 있습니다."
                )
            else :
                message = (
                    "봇에 등록된 사용자 정보를 모두 삭제하는 명령어입니다." "\n"
                    "데이터를 모두 삭제하시려면 /" + CMD['STOP'] + " ALL 을 입력해주세요." "\n"
                    "삭제된 키워드 정보는 복구되지 않습니다."
                )
            context.bot.send_message(chat_id=senderId, text=message)

    def help_(self, update, context) :
        if update.effective_chat.type == "private" :
            # only available in private chat
            CMD = self.CMD
            senderId = update.effective_chat.id
            message = (
                "/" + CMD['KADD'] + " <i>[keyword]</i> : 알람을 받을 키워드를 추가합니다." "\n"
                "/" + CMD['KDEL'] + " <i>[keyword]</i> : 등록된 키워드를 삭제합니다." "\n"
                "/" + CMD['KLIST'] + " : 등록된 키워드를 표시합니다."
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

    def leftChatMember(self, update, context) : # 어차피 그룹 채팅에서만 작동?
        # 사용자가 그룹에서 나가면, 그 사용자의 그룹 등록 정보를 삭제함
        database = self.database

        URL = self.URL

        leftMemberId = update.message.left_chat_member.id
        groupId = update.effective_chat.id

        ''' GROUP쪽 데이터 삭제 '''
        # Todo#3
        storedGroupUsers = database.get(URL['GROUP'] + '/' + str(groupId) + URL['USER'])
        if storedGroupUsers == None :
            storedGroupUsers = {}
        
        if str(leftMemberId) not in storedGroupUsers.values() :
            pass
        else :
            for key, val in storedGroupUsers.items() :
                if val == str(leftMemberId) :
                    database.delete(URL['GROUP'] + '/' + str(leftMemberId) + URL['USER'] + '/' + key)
                    break
        
        ''' USER쪽 데이터 삭제 '''
        storedRegisteredGroups = database.get(URL['USER'] + '/' + str(leftMemberId) + URL['REGISTERED_GROUP'])
        if storedRegisteredGroups == None :
            storedRegisteredGroups = {}
        
        if str(groupId) not in storedRegisteredGroups.keys() :
            pass
        else :
            database.delete(URL['USER'] + '/' + str(leftMemberId) + URL['REGISTERED_GROUP'] + '/' + str(groupId))

    def newChatTitle(self, update, context) : # 어차피 그룹 채팅에서만 작동
        database = self.database
        
        URL = self.URL
        KEY = self.KEY

        groupId = update.effective_chat.id
        newGroupName = update.message.new_chat_title

        database.get(URL['GROUP'] + '/' + str(groupId) + URL['INFO'],
            { KEY['GROUPNAME'] : newGroupName }
        )
        # 이름 갱신

