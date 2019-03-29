import telegram
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import log
import DatabaseControl
import keywordMethod
import groupMethod

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

    ###############################################
    self.token = <BOT_TOKEN>
    self.DB = DatabaseControl.DatabaseControl(<PATH/TO/KEY>, <FIREBASE_URL>, self.log)
    ###############################################

    self.core = telegram.Bot(self.token)
    self.updater = Updater(self.token)
      
  def msgHandler(self, func) :
    self.updater.dispatcher.add_handler(MessageHandler(Filters.text, func))
  
  def cmdHandler(self, cmd, func) :                               
    self.updater.dispatcher.add_handler(CommandHandler(cmd, func))
  
  def initHandler(self) :
    k = keywordMethod.Keyword(self.DB, self.log)
    g = groupMethod.Group(self.DB, self.log)

    self.cmdHandler(CMD.GTOGGLE, g.groupToggle)
    self.cmdHandler(CMD.GLIST, g.groupList)
    self.cmdHandler(CMD.GDELETE, g.groupDelete)

    self.cmdHandler(CMD.KADD, k.keywordAdd)
    self.cmdHandler(CMD.KLIST, k.keywordList)
    self.cmdHandler(CMD.KDELETE, k.keywordDelete)

    self.cmdHandler(CMD.HELP, self.showHelp)
    self.cmdHandler(CMD.INFO, self.showInfo)
    self.cmdHandler(CMD.HOWTO, self,showHowto)

    self.cmdHandler(CMD.START, self.start)

    self.msgHandler(self.getMessage)
  
  def isPrivateMsg(self, update) :
    if update.message.chat['type'] == 'private' :
      # 봇에게 직접 메세지를 보낼 때
      return True
    else :
      return False

  def boot(self) :
    self.log.info("000", "Bot Start")
    self.initHandler() # 명령어를 활성화시킨다.

    self.updater.start_polling()
    self.updater.idle()
  
  # userFunc
  def start(self, bot, update) :
    if self.isPrivateMsg(update) == True : # 개인톡으로 start를 보내면 경고함
      update.message.reply_text(MSG.WELCOME)
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

      self.log.info(userID, "그룹 추가 : " + str(groupID))
      update.message.reply_text("현재 그룹을 키워드 알림 봇에 등록합니다.\n기타 명령은 봇과의 개인 대화에서만 작동합니다.")
    else :
      self.DB.update(userID, URL.USER + userID_URL + URL.GROUP + groupID_URL, { 'gname' : groupName })
      # 그룹 이름이 바뀌면 갱신, 근데 유저가 start를 입력 해야지만 갱신된다..
      
      self.log.warn(userID, "등록된 그룹 추가 시도 : " + str(groupID))
      update.message.reply_text("이미 등록된 그룹입니다.\n기타 명령은 봇과의 개인 대화에서만 작동합니다.")

  def showHelp(self, bot, update) :
    if self.isPrivateMsg(update) == False :
      # 개인 메세지가 아니면 실행안함
      return
    update.message.reply_text(MSG.CMDLIST)

  def showInfo(self, bot, update) :
    if self.isPrivateMsg(update) == False :
      return
    # update.message.reply_text("개발중인 봇입니다.")
    update.message.reply_html(MSG.INFO, disable_web_page_preview=True)

  def showHowto(self, bot, update) :
    if self.isPrivateMsg(update) == False :
      return
    update.message.reply_html(MSG.HOWTO)

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

      try :
        kList = list(udata['keyword'].values())
        gDict = udata['group'].items() # 사용자에게 등록된 그룹들
      except :
        continue # 키워드를 등록 안 한 사용자

      for item in gDict : 
        gid, gdata = item
        # 사용자 DB에 저장된 그룹 데이터
        # gid(alarm, gname)
        
        if groupID == gid and gdata['alarm'] == ON :
          # 2. 해당 그룹에 속한 유저를 찾는다.
          # 3. 해당 그룹의 알람이 켜져있는지 확인한다

          for kvalue in kList :
            if kvalue in message.lower() :
              # 4. 해당 유저의 키워드가 사용되었는지 확인한다
              notiMessage = "%s 님이 호출했습니다.\n그룹 이름 : %s\n메세지 내용 : %s" % (senderName, groupName, message)

              self.core.send_message(uid, notiMessage, parse_mode=telegram.ParseMode.HTML)
              self.log.info(uid, "알림 전송 : " + senderID + '/' + senderName + '/' + groupID + '/' + groupName + '/' + message)

              if groupName is not gdata['gname'] :
                # DB에 저장된 그룹이름과 맞지 않으면(그룹명이 갱신된 경우)
                self.DB.update(uid, URL.USER + '/' + str(uid) + URL.GROUP + '/' + str(gid), { 'gname' : groupName })
                # 갱신작업

              break

if __name__ == "__main__":
    knoti = keyNotiBot()
    knoti.boot()
