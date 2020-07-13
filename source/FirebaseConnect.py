import firebase_admin
from firebase_admin import db, credentials

from configparser import ConfigParser

class FirebaseConnect :
    def __init__(self, config) :
        self.URL = config['URL']
        self.KEY = config['KEY']

        FIREBASE_URL = config['FIREBASE']['URL']
        FIREBASE_CERTPATH = config['FIREBASE']['CERTPATH']

        cred = credentials.Certificate(FIREBASE_CERTPATH)
        firebase_admin.initialize_app(cred, { 'databaseURL' : FIREBASE_URL })

    def get(self, url, shallow=False) :
        # shallow=True 시 child 데이터(key-val의 val에 해당)를 True,False로만 가져옴
        return db.reference(url).get(shallow=shallow)
    
    def push(self, url, value="") :
        db.reference(url).push(value)
        # value를 json형태로 주지 않으면, key값이 자동으로 난수가 입력된다
    
    def update(self, url, value) :
        db.reference(url).update(value)

    def delete(self, url) :
        db.reference(url).delete()

    def set(self, url, value) :
        db.reference(url).set(value)
    
    
    ''' preset '''

    ''' GET '''
    def getKeywordDict(self, userId) :
        URL = self.URL

        keywords = self.get(URL['USER'] + '/' + str(userId) + URL['KEYWORD'])
        if keywords == None :
            return {}
        else :
            return keywords

    def getGroupDataAll(self, groupId) :
        URL = self.URL

        data = self.get(URL['GROUP'] + '/' + str(groupId))
        if data == None :
            return {}
        else :
            return data

    # Todo#3    
    def getUserDictFromGroup(self, groupId) :
        URL = self.URL

        users = self.get(URL['GROUP'] + '/' + str(groupId) + URL['USER'])
        if users == None :
            return {}
        else :
            return users

    def getGroupDictFromUser(self, userId) :
        URL = self.URL
        
        groups = self.get(URL['USER'] + '/' + str(userId) + URL['REGISTERED_GROUP'])
        if groups == None :
            return {}
        else :
            return groups

    def getGroupName(self, groupId) :
        URL = self.URL
        KEY = self.KEY

        return self.get(URL['GROUP'] + '/' + str(groupId) + URL['INFO'] + '/' + KEY['GROUPNAME'])

    def getDoNotDisturb(self, userId) :
        URL = self.URL
        KEY = self.KEY

        start = self.get(URL['USER'] + '/' + str(userId) + URL['DONOTDISTURB'] + '/' + KEY['DONOTDISTURB_START'])
        end = self.get(URL['USER'] + '/' + str(userId) + URL['DONOTDISTURB'] + '/' + KEY['DONOTDISTURB_END'])

        return start, end

    ''' ADD, UPDATE '''
    def addUserToGroup(self, userId, groupId) :
        URL = self.URL

        self.push(URL['GROUP'] + '/' + str(groupId) + URL['USER'], str(userId))

    def addGroupToUser(self, groupId, userId) :
        URL = self.URL

        self.update(URL['USER'] + '/' + str(userId) + URL['REGISTERED_GROUP'],
            { str(groupId) : True }
        )

    def addKeywordToUser(self, keyword, userId) :
        URL = self.URL

        self.push(URL['USER'] + '/' + str(userId) + URL['KEYWORD'], keyword)

    def addNewGroup(self, groupId, data) :
        URL = self.URL

        self.set(URL['GROUP'] + '/' + str(groupId), data)

    def setGroupName(self, groupId, groupName) :
        URL = self.URL
        KEY = self.KEY

        self.update(URL['GROUP'] + '/' + str(groupId) + URL['INFO'],
            { KEY['GROUPNAME'] : groupName }
        )

    def setDoNotDisturb(self, userId, start, end) :
        URL = self.URL
        KEY = self.KEY

        self.update(URL['USER'] + '/' + str(userId) + URL['DONOTDISTURB'],
            { KEY['DONOTDISTURB_START'] : start }
        )
        self.update(URL['USER'] + '/' + str(userId) + URL['DONOTDISTURB'],
            { KEY['DONOTDISTURB_END'] : end }
        )

    ''' DELETE '''
    def deleteUserFromGroup(self, userId_key, groupId) :
        URL = self.URL

        self.delete(URL['GROUP'] + '/' + str(groupId) + URL['USER'] + '/' + str(userId_key))

    def deleteGroupFromUser(self, groupId, userId) :
        URL = self.URL

        self.delete(URL['USER'] + '/' + str(userId) + URL['REGISTERED_GROUP'] + '/' + str(groupId))

    def deleteUser(self, userId) :
        URL = self.URL
        
        self.delete(URL['USER'] + '/' + str(userId))

    def deleteKeyword(self, keyword_key, userId) :
        URL = self.URL

        self.delete(URL['USER'] + '/' + str(userId) + URL['KEYWORD'] + '/' + keyword_key)

    def deleteGroup(self, groupId) :
        URL = self.URL

        self.delete(URL['GROUP'] + '/' + str(groupId))


    ''' PRESET '''
    def migrateGroupData(self, oldGroupId, newGroupId) :
        groupData = self.getGroupDataAll(oldGroupId)
        # 데이터 가져오기
        
        self.addNewGroup(newGroupId, groupData)
        # 새 그룹 아이디에 데이터 복사

        self.deleteGroup(oldGroupId)
        # 쓸모없어진 이전 데이터 삭제

    def migrateUserData(self, oldGroupId, newGroupId) :
        usersInGroup = self.getUserDictFromGroup(newGroupId)
        # 위의 migrateGroupData를 먼저 실행할 거니까, 여기서는 newGroupId를 기준으로 가져오는 것이 맞다.

        for key, userId in usersInGroup.items() :
            # 그룹에 등록된 사용자들에게서 등록된 그룹목록을 가져옴 아따 복잡하다 ㅋㅋ 왜 이렇게 만들었니?
            groupsInUser = self.getGroupDictFromUser(userId)

            for groupId in groupsInUser.keys() :
                if groupId == str(oldGroupId) :
                    self.deleteGroupFromUser(oldGroupId, userId)
                    # 이전 그룹 아이디를 삭제하고
                    self.addGroupToUser(newGroupId, userId)
                    # 새 그룹 아이디를 추가