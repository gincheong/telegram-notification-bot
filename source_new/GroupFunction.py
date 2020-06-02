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

            URL = self.URL
            KEY = self.KEY

            senderId = update.effective_chat.id

            storedGroups = database.get(URL['USER'] + '/' + str(senderId) + '/' + URL['REGISTERED_GROUP'], shallow=True)

            if storedGroups == None :
                message = (
                    "등록된 그룹이 없습니다."
                )
            else :
                groupNameList = []
                for groupId in storedGroups.keys() : # key쪽에 id가 입력됨
                    # find groupname
                    groupName = database.get(URL['GROUP'] + '/' + str(groupId) + URL['INFO'] + '/' + KEY['GROUPNAME'])
                    groupNameList.append(groupName)
                message = (
                    "등록된 그룹 목록입니다." "\n" +
                    "\n".join(groupNameList)
                )

            context.bot.send_message(chat_id=senderId, text=message)