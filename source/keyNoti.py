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
    self.updater = Updater(self.token, use_context=True)
    # https://github.com/python-telegram-bot/python-telegram-bot/wiki/Transition-guide-to-Version-12.0#what-exactly-is-callbackcontext
    # 12버전으로 코드 바꾸기
      
  def msgHandler(self, func) :
    self.updater.dispatcher.add_handler(MessageHandler(Filters.text, func))
    # self.updater.dispatcher.add_handler(MessageHandler(Filters.status_update.left_chat_member, func))
  
  def cmdHandler(self, cmd, func) :                               
    self.updater.dispatcher.add_handler(CommandHandler(cmd, func))
  
  def initHandler(self) :
    k = keywordMethod.Keyword(self.DB, self.log)
    g = groupMethod.Group(self.DB, self.log)

    # self.cmdHandler(CMD.GTOGGLE, g.groupToggle) # deprecated
    self.cmdHandler(CMD.GLIST, g.groupList)
    # self.cmdHandler(CMD.GDELETE, g.groupDelete)

    self.cmdHandler(CMD.KADD, k.keywordAdd)
    self.cmdHandler(CMD.KLIST, k.keywordList)
    self.cmdHandler(CMD.KDELETE, k.keywordDelete)
    self.msgHandler(k.checkMessage)

    self.cmdHandler(CMD.HELP, self.showHelp)
    # self.cmdHandler(CMD.INFO, self.showInfo)
    self.cmdHandler(CMD.HOWTO, self.showHowto)

    self.cmdHandler(CMD.START, self.start)
    # self.cmdHandler(CMD.DISABLE, self.disableNotification) # deprecated
    # self.cmdHandler(CMD.ENABLE, self.enableNotification) # deprecated
  
  def isPrivateMsg(self, update) :
    if update.message.chat['type'] == 'private' :
      # 봇에게 직접 메세지를 보낼 때
      return True
    else :
      return False

  def boot(self) :
    self.log.info("000", "Bot Start")
    self.initHandler() # 명령어를 활성화시킨다.
    print('bot started')

    self.updater.start_polling()
    self.updater.idle()
  
  # userFunc
  def start(self, bot, update) :
    if self.isPrivateMsg(update) == True :
      # 봇 최초 실행 시에 이리로 오는 것이기도 함
      update.message.reply_text(MSG.WELCOME)
      update.message.reply_html(MSG.PREVIEW)
      update.message.reply_html(MSG.INFO, disable_web_page_preview=True)
      return

    groupID = str(update.message.chat['id'])
    groupName = update.message.chat['title']
    userID = str(update.message.from_user['id'])

    # 1124 new code
    savedGroup = self.DB.get(userID, URL.GROUP + '/' + groupID)
    
    if savedGroup == None :
      # 등록되지 않은 그룹인 경우
      self.DB.update(userID, URL.GROUP + '/' + groupID + URL.INFO, { 'groupname' : groupName })
      # info 아래에 그룹 이름 추가
      self.DB.push(userID, URL.GROUP + '/' + groupID + URL.USER, userID)
      # 사용자 목록에 추가
    else :
      # 이미 등록된 그룹인 경우
      savedGroupName = savedGroup['info']['groupname']
      if groupName is not savedGroupName :
        self.DB.update(userID, URL.GROUP + '/' + groupID + URL.INFO, { 'groupname' : groupName })
      # 그룹이름이 달라졌을 경우 갱신함

      # 사용자가 그룹에 등록되어 있는지 확인..
      savedGroupUser = self.DB.get(userID, URL.GROUP + '/' + groupID + URL.USER)
      
      if savedGroupUser == None :
        # 해당 그룹에 등록자가 하나도 없는 경우, 그룹ID만 껍데기로 존재
        self.DB.push(userID, URL.GROUP + '/' + groupID + URL.USER, userID)
        # 새로 추가함
        self.log.info(userID, "그룹 추가 : " + groupID)
        update.message.reply_text("현재 그룹을 키워드 알림 봇에 등록합니다.\n기타 명령은 봇과의 개인 대화에서만 작동합니다.")
        return

      if userID not in savedGroupUser.values() :
        # /start 입력한 사용자 ID가 그룹 내 사용자 목록에 없으면
        self.DB.push(userID, URL.GROUP + '/' + groupID + URL.USER, userID)
        # 새로 추가함
        self.log.info(userID, "그룹 추가 : " + groupID)
        update.message.reply_text("현재 그룹을 키워드 알림 봇에 등록합니다.\n기타 명령은 봇과의 개인 대화에서만 작동합니다.")
      else :
        # 이미 등록되어 있으면
        self.log.warn(userID, "이미 등록된 그룹 추가 시도 : " + groupID)
        update.message.reply_text("이미 등록된 그룹입니다.\n기타 명령은 봇과의 개인 대화에서만 작동합니다.")

  def showHelp(self, bot, update) :
    if self.isPrivateMsg(update) == False :
      # 개인 메세지가 아니면 실행안함
      return
    update.message.reply_text(MSG.CMDLIST)

  # DEPRECATED / INFO 내용을 start 메세지에 추가함
  # def showInfo(self, bot, update) :
  #   if self.isPrivateMsg(update) == False :
  #     return
  #   update.message.reply_html(MSG.INFO, disable_web_page_preview=True)

  def showHowto(self, bot, update) :
    if self.isPrivateMsg(update) == False :
      return
    update.message.reply_html(MSG.HOWTO)