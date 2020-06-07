from configparser import ConfigParser

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

class GroupFunction :
    def __init__(self, config, database) :
        self.database = database
        
        self.URL = config['URL']
        self.KEY = config['KEY']
        self.CMD = config['CMD']

    def glist(self, update, context) :
        if update.effective_chat.type == "private" :
            database = self.database

            senderId = update.effective_chat.id

            storedGroups = database.getGroupDictFromUser(senderId)

            if len(storedGroups) == 0 :
                message = (
                    "등록된 그룹이 없습니다."
                )
            else :
                groupNameList = []
                for groupId in storedGroups.keys() : # key쪽에 id가 입력됨
                    # find groupname
                    groupName = database.getGroupName(groupId)
                    groupNameList.append(groupName)
                message = (
                    "등록된 그룹 목록입니다." "\n" +
                    "\n".join(groupNameList)
                )

            context.bot.send_message(chat_id=senderId, text=message)