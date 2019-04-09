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
from constants import Bool as B

# /setprivacy DISABLED # 명령이 아닌 그룹 메세지에도 반응

class keyNotiBot :
  def __init__(self, token, key, url) :
    self.log = log.Log()
    self.log.info("000", "Program Start")

    self.token = token
    self.DB = DatabaseControl.DatabaseControl(key, url, self.log)

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
    self.msgHandler(k.checkMessage)

    self.cmdHandler(CMD.HELP, self.showHelp)
    self.cmdHandler(CMD.INFO, self.showInfo)
    self.cmdHandler(CMD.HOWTO, self.showHowto)

    self.cmdHandler(CMD.START, self.start)
    self.cmdHandler(CMD.DISABLE, self.disableNotification)
    self.cmdHandler(CMD.ENABLE, self.enableNotification)
  
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
      update.message.reply_html(MSG.PREVIEW)
      return

    groupID = update.message.chat['id']
    groupName = update.message.chat['title']
    userID = update.message.from_user['id']
    userID_URL = '/' + str(userID)
    groupID_URL = '/' + str(groupID)
    
    groupList = self.DB.get(userID, URL.USER + userID_URL + URL.GROUP)
    
    if groupList == None or str(groupID) not in groupList.keys()  : # 신규등록
      self.DB.update(userID, URL.USER + userID_URL + URL.GROUP + groupID_URL, { 'alarm' : B.ON })
      self.DB.update(userID, URL.USER + userID_URL + URL.GROUP + groupID_URL, { 'gname' : groupName })

      self.log.info(userID, "그룹 추가 : " + str(groupID))
      update.message.reply_text("현재 그룹을 키워드 알림 봇에 등록합니다.\n기타 명령은 봇과의 개인 대화에서만 작동합니다.")
    else :
      self.DB.update(userID, URL.USER + userID_URL + URL.GROUP + groupID_URL, { 'gname' : groupName })
      # 그룹 이름이 바뀌면 갱신, 근데 유저가 start를 입력 해야지만 갱신된다..
      
      self.log.warn(userID, "등록된 그룹 추가 시도 : " + str(groupID))
      update.message.reply_text("이미 등록된 그룹입니다.\n기타 명령은 봇과의 개인 대화에서만 작동합니다.")

    notiState = self.DB.get(userID, URL.USER + userID_URL + URL.CONFIG)

    if notiState == None :
      self.DB.update(userID, URL.USER + userID_URL + URL.CONFIG, { 'notification' : B.ON })    

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

  def enableNotification(self, bot, update) :
    if self.isPrivateMsg(update) == False :
      return
      
    userID = update.message.chat['id']
    userID_URL = '/' + str(userID)

    self.DB.update(userID, URL.USER + userID_URL + URL.CONFIG, { 'notification' : B.ON })
    update.message.reply_text("전체 키워드 알림을 ON합니다.")
    self.log.info(userID, "전체 알림 ON 설정")

  def disableNotification(self, bot, update) :
    if self.isPrivateMsg(update) == False :
      return
    
    userID = update.message.chat['id']
    userID_URL = '/' + str(userID)
    
    self.DB.update(userID, URL.USER + userID_URL + URL.CONFIG, { 'notification' : B.OFF })
    update.message.reply_text("전체 키워드 알림을 OFF합니다.")
    self.log.info(userID, "전체 알림 OFF 설정")