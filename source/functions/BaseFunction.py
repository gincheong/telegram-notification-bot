from configparser import ConfigParser

class BaseFunction :
    def __init__(self, config, database, logger) :
        self.database = database
        self.logger = logger
        
        self.URL = config['URL']
        self.KEY = config['KEY']
        self.CMD = config['CMD']

    def start(self, update, context) :
        # Private Chat
        if update.effective_chat.type == "private" :
            senderId = update.effective_chat.id

            message = (
                "키워드 감지를 위해 봇이 메시지에 접근할 수 있습니다. (Group Privacy Disabled)" "\n"
                "키워드 감지 시에만 메세지 내용에 접근하며, 내용은 절대 기록하지 않습니다." "\n"
                "봇은 지난 메시지에 접근할 권한이 없습니다." "\n"
                "데이터베이스에는 그룹 이름만이 저장되며, 기타 사용자 이름이나 메세지 등은 저장되지 않습니다." "\n"
                "키워드 데이터는 암호화하지 않고 저장하므로 중요한 개인정보를 입력하지 마세요."
            )
            context.bot.send_message(chat_id=senderId, text=message)

            message = (
                'Github : <a href="https://github.com/gincheong/telegram-notification-bot">telegram-notification-bot</a>' "\n"
                "Telegram : @gincheong" "\n"
                "오류 발생 시 텔레그램으로 문의 바랍니다."
            )
            context.bot.send_message(chat_id=senderId, text=message, disable_web_page_preview=True, parse_mode="html")

            message = (
                "내가 등록한 키워드가 그룹 채팅방에서 사용되면, 봇이 메시지를 전송합니다." "\n"
                "/howto 명령어로 사용방법을 확인하세요."
            )
            context.bot.send_message(chat_id=senderId, text=message)

        # Group Chat
        elif update.effective_chat.type == "group" :
            database = self.database
            
            senderId = update.message.from_user.id
            messageId = update.message.message_id

            groupId = update.effective_chat.id
            groupName = update.effective_chat.title

            # Firebase 연결

            ''' GROUP 쪽 데이터 작업 '''
            # 그룹 신규 등록 or 그룹 이름 최신화
            database.setGroupName(groupId, groupName)
            
            # Todo#3
            storedGroupUsers = database.getUserDictFromGroup(groupId) # GROUP쪽에 등록된 사용자 목록

            if str(senderId) not in storedGroupUsers.values() :
                # 신규 등록
                database.addUserToGroup(senderId, groupId)
            else :
                pass

            ''' USER 쪽 데이터 '''
            storedRegisteredGroups = database.getGroupDictFromUser(senderId)

            if str(groupId) not in storedRegisteredGroups.keys() :
                # 신규 등록
                database.addGroupToUser(groupId, senderId)
                message = (
                    "현재 그룹을 키워드 알림 봇에 등록합니다." "\n"
                    "기타 명령어는 봇과의 개인 대화에서만 작동합니다."
                )
                self.logger.info("New Group Added : uid:{}, gid:{}".format(senderId, groupId))
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

            senderId = update.message.from_user.id
            messageId = update.message.message_id

            groupId = update.effective_chat.id

            ''' GROUP쪽 데이터 삭제 '''
            storedGroupUsers = database.getUserDictFromGroup(groupId)

            if str(senderId) not in storedGroupUsers.values() :
                pass
            else : 
                for key, val in storedGroupUsers.items() :
                    if val == str(senderId) :
                        database.deleteUserFromGroup(key, groupId)
                        break

            ''' USER쪽 데이터 삭제 '''
            storedRegisteredGroups = database.getGroupDictFromUser(senderId)
            
            if str(groupId) not in storedRegisteredGroups.keys() :
                message = (
                    "등록되지 않은 그룹입니다."
                )
            else :
                database.deleteGroupFromUser(groupId, senderId)
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

            senderId = update.effective_chat.id
            senderMessage = update.message.text

            
            if senderMessage == ("/" + CMD['STOP'] + " ALL") :
                # registered_group 통해서, GROUP 쪽에 등록된 사용자 아이디 모두 지우기
                ''' GROUP쪽 데이터 삭제 '''
                storedRegisteredGroups = database.getGroupDictFromUser(senderId)

                if len(storedRegisteredGroups) == 0 :
                    pass
                else :
                    # 비효율의 끝..?
                    for eachGroupId, val in storedRegisteredGroups.items() :
                        # USER에 저장된 groupId를 가지고, GROUP쪽을 돌면서 삭제함
                        storedGroupUsers = database.getUserDictFromGroup(eachGroupId)

                        if str(senderId) not in storedGroupUsers.values() :
                            pass
                        else :
                            for key, val in storedGroupUsers.items() :
                                if val == str(senderId) :
                                    database.deleteUserFromGroup(key, eachGroupId)
                                    break

                ''' USER쪽 데이터 삭제 '''
                database.deleteUser(senderId)
                self.logger.info("Delete User Data : uid:{}".format(senderId))

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
            
            # 그룹 채팅방과 개인 채팅방 명령어를 나누기
            message = (
                "[개인 채팅 내 명령어]" "\n"
                "/" + CMD['KADD'] + " <i>[keyword]</i> : 알람을 받을 키워드를 추가합니다." "\n"
                "/" + CMD['KDEL'] + " <i>[keyword]</i> : 등록된 키워드를 삭제합니다." "\n" 
                "/" + CMD['KLIST'] + " : 등록된 키워드를 표시합니다." "\n"
                "/" + CMD['GLIST'] + " : 등록된 그룹을 표시합니다." "\n"
                "/" + CMD['HELP'] + " : 현재 메세지를 표시합니다." "\n"
                "/" + CMD['HOWTO'] + " : 간단한 봇 사용법을 표시합니다." "\n"
                "/" + CMD['STOP'] + " : 봇에 등록된 사용자 정보를 모두 삭제합니다." "\n"
                "/" + CMD['START'] + " : 봇에 대한 설명을 볼 수 있습니다."
            )
            context.bot.send_message(chat_id=senderId, text=message, parse_mode="html")
            
            message = (
                "[그룹 채팅 내 명령어]" "\n"
                "/" + CMD['START'] + " : 현재 그룹을 봇에 등록합니다." "\n"
                "/" + CMD['DELETE'] + " : 현재 그룹을 봇에서 등록 해제합니다."
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

        leftMemberId = update.message.left_chat_member.id
        groupId = update.effective_chat.id

        ''' GROUP쪽 데이터 삭제 '''
        storedGroupUsers = database.getUserDictFromGroup(groupId)
        
        if str(leftMemberId) not in storedGroupUsers.values() :
            pass
        else :
            for key, val in storedGroupUsers.items() :
                if val == str(leftMemberId) :
                    database.deleteUserFromGroup(key, groupId)
                    break
        
        ''' USER쪽 데이터 삭제 '''
        storedRegisteredGroups = database.getGroupDictFromUser(leftMemberId)
        
        if str(groupId) not in storedRegisteredGroups.keys() :
            pass
        else :
            database.deleteGroupFromUser(groupId, leftMemberId)

    def newChatTitle(self, update, context) : # 어차피 그룹 채팅에서만 작동
        database = self.database
        
        groupId = update.effective_chat.id
        newGroupName = update.message.new_chat_title

        database.setGroupName(groupId, newGroupName)
        # 이름 갱신

