import telegram
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import log
import DatabaseControl
from constants import Command as CMD
from constants import FirebaseURL as URL
from constants import Message as MSG
from constants import Bool as B

class Group :
  def __init__(self, DB, log) :
    self.DB = DB
    self.log = log

  def isPrivateMsg(self, update) :
    if update.message.chat['type'] == 'private' :
      # 봇에게 직접 메세지를 보낼 때
      return True
    else :
      return False

  # 200525
  def groupList(self, bot, update) :
    if self.isPrivateMsg(update) == False :
      # 개인 메세지일때만 실행
      return

    userID = str(update.message.chat['id'])
    userID_URL = '/' + userID
    groupData = self.DB.get(userID, URL.USER + userID_URL + URL.REGISTERED_GROUP)
    
    fullMessage = "등록된 그룹 목록입니다."
    # messageFormat = "{}. [{}] {}"
    messageFormat = "{}. {}"

    for idx, groupData in enumerate(groupData.items()) :
      groupID, alarm = groupData
      groupID_URL = '/' + str(groupID)
      groupName = self.DB.get(userID, URL.GROUP + groupID_URL + URL.INFO)['groupname']

      alarm = str(alarm).replace('True', 'ON').replace('False', 'OFF')
      
      # 알람설정하는거 없어서 우선 ON OFF 표시 안하기
      # fullMessage += '\n' + messageFormat.format(idx+1, alarm, groupName)
      fullMessage += '\n' + messageFormat.format(idx+1, groupName)

    update.message.reply_text(fullMessage)

  def groupDelete(self, bot, update) :
    if self.isPrivateMsg(update) == True :
      # 개인 메시지로 작동하지 않음
      # 해당 그룹 채팅방에서 삭제함
      return
    
    groupID = str(update.message.chat['id'])
    userID = str(update.message.from_user['id'])

    groupDict = self.DB.get(userID, URL.GROUP + '/' + groupID)

    if groupDict == None :
      # 그룹 자체가 데이터베이스에 등록되지 않은 경우
      update.message.reply_text("등록되지 않은 그룹입니다.")
      return
    
    # 그룹이 등록은 되어있는데
    for key, val in groupDict['user'].items() :
      if val == userID :
        # 해당 그룹에 등록된 사용자 목록에 현재 사용자가 있으면
        self.DB.delete(userID, URL.GROUP + '/' + groupID + URL.USER + '/' + key)
        # 키 값으로 데이터 삭제
        update.message.reply_text("현재 그룹을 등록 해제했습니다.")
        self.log.info(userID, "그룹 삭제 : " + str(groupID))
        break
      else :
        # 목록에 현재 사용자가 없으면
        update.message.reply_text("등록되지 않은 그룹입니다.")