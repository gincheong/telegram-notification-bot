import telegram
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import log
import DatabaseControl
from constants import Command as CMD
from constants import FirebaseURL as URL
from constants import Message as MSG

# /setprivacy DISABLED # 명령이 아닌 그룹 메세지에도 반응

ON = 1
OFF = 0

class keyNotiBot :
  def __init__(self) :
    self.log = log.Log()
    self.log.info("000", "Program Start")
    # 기록용
    ###############################################
    self.token = <BOT_TOKEN>
    self.DB = DatabaseControl.DatabaseControl(<PATH/TO/KEY>, <FIREBASE_URL>, self.log)
    ###############################################

    self.core = telegram.Bot(self.token)
    self.updater = Updater(self.token)

  def isPrivateMsg(self, update) :
    if update.message.chat['type'] == 'private' :
      # 봇에게 직접 메세지를 보낼 때
      return True
    else :
      return False
      
  def msgHandler(self, func) :
    self.updater.dispatcher.add_handler(MessageHandler(Filters.text, func))
  
  def cmdHandler(self, cmd, func) :                               
    self.updater.dispatcher.add_handler(CommandHandler(cmd, func))
  
  def initHandler(self) :
    self.cmdHandler(CMD.TOGGLE, self.alarmToggle)
    self.cmdHandler(CMD.KEYWORD, self.addKeyword)
    self.cmdHandler(CMD.HELP, self.cmdHelp)
    self.cmdHandler(CMD.LIST, self.showList)
    self.cmdHandler(CMD.DELETE, self.deleteKeyword)
    self.cmdHandler(CMD.INFO, self.showInfo)
    self.cmdHandler(CMD.START, self.start)

    self.msgHandler(self.getMessage)

  def alarmToggle(self, bot, update) :
    if self.isPrivateMsg(update) == False :
      # 개인 메세지가 아니면 실행 안함
      return
    
    userInput = update.message.text
    userID = update.message.chat['id']
    userID_URL = '/' + str(userID)

    groupDict = self.DB.get(userID, URL.USER + userID_URL + URL.GROUP)
    try :
      groupList = list(groupDict)
      numberOfGroup = len(groupList)
    except :
      update.message.reply_text("등록된 그룹이 없습니다.")
      

    alarmState = list()
    for i in range(numberOfGroup) :
      if groupDict[groupList[i]]['alarm'] == ON :
        alarmState.append("ON")
      elif groupDict[groupList[i]]['alarm'] == OFF :
        alarmState.append("OFF")

    if userInput == ("/" + CMD.TOGGLE) : # 아무 키워드도 입력하지 않음
      msg = "등록된 그룹 목록입니다."
      for i in range(numberOfGroup) :
        msg += "\n" + str(i) + ". " + groupDict[groupList[i]]['gname'] + " : " + alarmState[i]
      update.message.reply_text(msg)
      update.message.reply_text("알람을 활성화/비활성화 하려는 그룹의 번호를 같이 입력해 주세요.\n" + \
            "ex> /toggle 1 (1번 그룹의 알람 활성화/비활성화)")
    else : # 내용을 입력받은 경우
      groupNo = userInput[8 : ].strip()

      try :
        groupNo = int(groupNo) # 정수인지 확인
      except :
        update.message.reply_text("잘못된 입력입니다.")
        return

      if groupNo < numberOfGroup : # 유효한 번호인가
        if alarmState[groupNo] == "ON" :
          groupID_URL = '/' + str(groupList[groupNo])

          self.DB.update(userID, URL.USER + userID_URL + URL.GROUP + groupID_URL, { 'alarm' : OFF })

          self.log.info(userID, str(groupList[i]) + "의 알림을 OFF로 변경")
          update.message.reply_text("해당 그룹의 알림을 OFF했습니다.")
        elif alarmState[groupNo] == "OFF" :
          self.DB.update(userID, URL.USER + userID_URL + URL.GROUP + groupID_URL, { 'alarm' : ON })
          
          self.log.info(userID, str(groupList[i]) + "의 알림을 ON으로 변경")
          update.message.reply_text("해당 그룹의 알림을 ON했습니다.")
      else :
        update.message.reply_text("유효하지 않은 번호입니다.")
      
  def boot(self) :
    self.log.info("000", "Bot Start")
    self.initHandler() # 명령어를 활성화시킨다.

    self.updater.start_polling()
    self.updater.idle()
  
  # userFunc
  def start(self, bot, update) :
    if self.isPrivateMsg(update) == True : # 개인톡으로 start를 보내면 경고함
      update.message.reply_text(MSG.WARN)
      return

    groupID = update.message.chat['id']
    groupName = update.message.chat['title']
    userID = update.message.from_user['id']
    userID_URL = '/' + str(userID)
    groupID_URL = '/' + str(groupID)
    
    groupList = self.DB.get(userID, URL.USER + userID_URL + URL.GROUP)
    
    if groupList == None or str(groupID) not in groupList.keys()  : # 신규등록
      self.DB.update(userID, URL.USER + userID_URL + URL.GROUP + groupID_URL, { 'alarm' : ON })
      self.DB.update(userID, URL.USER + userID_URL + URL.GROUP + groupID_URL, { 'gname' : groupName })

      self.log.info(userID, "그룹을 추가했습니다. " + str(groupID))
      update.message.reply_text("현재 그룹을 키워드 알림 봇에 등록합니다.")
    else :
      self.DB.update(userID, URL.USER + userID_URL + URL.GROUP + groupID_URL, { 'gname' : groupName })
      # 그룹 이름이 바뀌면 갱신, 근데 유저가 start를 입력 해야지만 갱신된다..
      
      self.log.warn(userID, "이미 등록된 그룹 추가 시도. " + str(groupID))
      update.message.reply_text("이미 등록된 그룹입니다.")

  def cmdHelp(self, bot, update) :
    if self.isPrivateMsg(update) == False :
      # 개인 메세지가 아니면 실행안함
      return
    update.message.reply_text(MSG.CMDLIST)

  # 그룹 메세지를 읽어서 키워드를 확인하는 함수
  def getMessage(self, bot, update) :
    if self.isPrivateMsg(update) == True :
      # 봇에게 보낸 개인 메세지면 무시함
      return
    
    '''
    1. 어느 그룹인지 확인한다
    2. db에서 해당 그룹에 속한 유저를 조회한다
    #. 보낸 사람은 유저 목록에서 제외해야함
    3. 해당 그룹의 알람이 켜져있는지 확인한다
    4. 해당 유저의 키워드가 사용되었는지 확인한다
    5. 알림을 보낸다
    '''
    message = update.message.text
    senderID = str(update.message.from_user['id'])
    groupID = str(update.message.chat['id'])
    groupName = update.message.chat['title']
    # 1. 그룹을 확인한다
    
    try :
      senderName = update.message.from_user['last_name'] + " " + update.message.from_user['first_name']
    except : # last name을 등록 안 하는 경우
      senderName = update.message.from_user['first_name']

    allUser = self.DB.get('000', URL.USER)

    for uid, udata in allUser.items() :
      if uid == senderID :
        continue # 메세지 보낸 당사자에게는 알리지 않는다.

      kList = list(udata['keyword'].values())
      gDict = udata['group'].items() # 사용자에게 등록된 그룹들

      for item in gDict :
        gid, gdata = item
        
        if groupID == gid and gdata['alarm'] == ON :
          # 2. 해당 그룹에 속한 유저를 찾는다.
          # 3. 해당 그룹의 알람이 켜져있는지 확인한다

          for kvalue in kList :
            if kvalue in message :
              # 4. 해당 유저의 키워드가 사용되었는지 확인한다
              message = message.replace(kvalue, '<b>' + kvalue + '</b>')
              notiMessage = senderName + " 님이 호출했습니다.\n" + \
                            "그룹 이름 : " + groupName + "\n" + \
                            "메세지 내용 : " + message
              self.core.send_message(uid, notiMessage, parse_mode=telegram.ParseMode.HTML)
              self.log.info(uid, "알림을 보냈습니다. " + senderID + '/' + senderName + '/' + groupID + '/' + groupName + '/' + message)
              break

  def addKeyword(self, bot, update) :
    if self.isPrivateMsg(update) == False :
      # 개인 메세지가 아니면 실행안함
      return

    userID = update.message.chat['id']
    userInput = update.message.text

    if userInput == ("/" + CMD.KEYWORD) :
      update.message.reply_text("추가할 키워드를 입력해주세요.\n" + \
        "ex> /keyword 안녕 (\"안녕\" 키워드 추가)")
          # 사용법 보여줌
    else :
      newKeyword = userInput[9 : ].strip()
      keywordDict = self.DB.get(userID, URL.USER + '/' + str(userID) +URL.KEYWORD)
      
      if keywordDict == None or newKeyword not in keywordDict.values() :
        self.DB.push(userID, URL.USER + '/' + str(userID) +URL.KEYWORD, newKeyword)

        self.log.info(userID, "키워드 추가 : " + newKeyword)
        update.message.reply_html("<b>" + newKeyword + "</b> 키워드를 추가했습니다.")
      else :
        update.message.reply_text("이미 등록된 키워드입니다.")

  def showList(self, bot, update) :
    if self.isPrivateMsg(update) == False :
      return

    userID = update.message.chat['id']
    keywordDict = self.DB.get(userID, URL.USER + '/' + str(userID) + URL.KEYWORD)

    try :
      update.message.reply_html("등록된 키워드 목록입니다.\n" + \
                        "<b>" + ", ".join(keywordDict.values()) + "</b>")
    except :
      update.message.reply_text("등록된 키워드가 없습니다.")
  
  def deleteKeyword(self, bot, update) :
    if self.isPrivateMsg(update) == False :
      return

    userID = update.message.chat['id']
    userInput = update.message.text

    if userInput == ('/' + CMD.DELETE) :
      update.message.reply_text("삭제할 키워드를 입력하세요.\n" + \
        "ex> /delete 안녕 (\"안녕\" 키워드 삭제)")
    else :
      deleteKeyword = userInput[8 : ].strip()
      keywordDict = self.DB.get(userID, URL.USER + '/' + str(userID) + URL.KEYWORD)
      
      if keywordDict == None :
        update.message.reply_text("등록된 키워드가 없습니다.")
      elif deleteKeyword not in keywordDict.values() :
        update.message.reply_text("등록되지 않은 키워드입니다.")
      else :
        for key, value in keywordDict.items() :
          if deleteKeyword == value :
            self.DB.delete(userID, URL.USER + '/' + str(userID) + URL.KEYWORD + '/' + key)
            break
        
        update.message.reply_html("<b>" + deleteKeyword + "</b> 키워드를 삭제했습니다.")
        self.log.info(userID, deleteKeyword + " 키워드를 삭제했습니다.")

  def showInfo(self, bot, update) :
    if self.isPrivateMsg(update) == False :
      return

    update.message.reply_text("개발중인 봇입니다.")
    update.message.reply_html(MSG.INFO, disable_web_page_preview=True)

if __name__ == "__main__":
    knoti = keyNotiBot()
    knoti.boot()
