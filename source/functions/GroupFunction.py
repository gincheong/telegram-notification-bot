from configparser import ConfigParser

class GroupFunction :
    def __init__(self, config, database, logger) :
        self.database = database
        self.logger = logger
        
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
                self.logger.info("glist NoData : uid:{}".format(senderId))
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
                self.logger.info("glist Success : uid:{}".format(senderId))

            context.bot.send_message(chat_id=senderId, text=message)