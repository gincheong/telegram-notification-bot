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

  def groupToggle(self, bot, update) :
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
      return

    alarmState = list()
    for i in range(numberOfGroup) :
      if groupDict[groupList[i]]['alarm'] == B.ON :
        alarmState.append("ON")
      elif groupDict[groupList[i]]['alarm'] == B.OFF :
        alarmState.append("OFF")
    
    msg = "등록된 그룹 목록입니다."
    if userInput == ("/" + CMD.GTOGGLE) : # 아무 키워드도 입력하지 않음
      for i in range(numberOfGroup) :
        msg += '\n' + str(i) + '. ' + groupDict[groupList[i]]['gname'] + ' : ' + alarmState[i]
      update.message.reply_text(msg)
      update.message.reply_text("알람을 활성화/비활성화 하려는 그룹의 번호를 같이 입력해 주세요.\n" + \
            "ex> /gtoggle 1 (1번 그룹의 알람 활성화/비활성화)")
    else : # 내용을 입력받은 경우
      groupNo = userInput[len(CMD.GTOGGLE) + 2 : ].strip()

      try :
        groupNo = int(groupNo) # 정수인지 확인
      except :
        update.message.reply_text("잘못된 입력입니다.")
        return

      if groupNo < numberOfGroup : # 유효한 번호인가
        groupName = groupDict[groupList[groupNo]]['gname']

        if alarmState[groupNo] == "ON" :
          groupID_URL = '/' + str(groupList[groupNo])

          self.DB.update(userID, URL.USER + userID_URL + URL.GROUP + groupID_URL, { 'alarm' : B.OFF })

          self.log.info(userID, str(groupList[i]) + "의 알림을 OFF로 변경")
          update.message.reply_html("<b>" + groupName + "</b> 그룹의 알림을 OFF했습니다.")
        elif alarmState[groupNo] == "OFF" :
          groupID_URL = '/' + str(groupList[groupNo])
          
          self.DB.update(userID, URL.USER + userID_URL + URL.GROUP + groupID_URL, { 'alarm' : B.ON })
          
          self.log.info(userID, str(groupList[i]) + "의 알림을 ON으로 변경")
          update.message.reply_html("<b>" + groupName + "</b> 그룹의 알림을 ON했습니다.")
      else :
        update.message.reply_text("유효하지 않은 번호입니다.")

  def groupList(self, bot, update) :
    if self.isPrivateMsg(update) == False :
      # 개인 메세지가 아니면 실행 안함
      return

    userID = update.message.chat['id']
    userID_URL = '/' + str(userID)

    groupDict = self.DB.get(userID, URL.USER + userID_URL + URL.GROUP)

    try :
      groupList = list(groupDict)
      numberOfGroup = len(groupList)
    except :
      update.message.reply_text("등록된 그룹이 없습니다.")
      return
    
    alarmState = list()
    for i in range(numberOfGroup) :
      if groupDict[groupList[i]]['alarm'] == B.ON :
        alarmState.append("ON")
      elif groupDict[groupList[i]]['alarm'] == B.OFF :
        alarmState.append("OFF")

    msg = "등록된 그룹 목록입니다."
    for i in range(numberOfGroup) :
      msg += '\n' + str(i) + '. ' + groupDict[groupList[i]]['gname'] + ' : ' + alarmState[i]
    update.message.reply_text(msg)

  def groupDelete(self, bot, update) :
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
      return

    msg = "등록된 그룹 목록입니다."
    if userInput == ('/' + CMD.GDELETE) :
      for i in range(numberOfGroup) :
        msg += '\n' + str(i) + '. ' + groupDict[groupList[i]]['gname'] + ' : ' + alarmState[i]
      update.message.reply_text(msg)
      update.message.reply_text("삭제할 그룹의 번호를 같이 입력해 주세요.\n" + \
            "ex> /gdel 0 (0번 그룹을 삭제)")
    else : # 번호 입력이 있었으면
      groupNo = userInput[len(CMD.GDELETE) + 2 : ].strip()

      try :
        groupNo = int(groupNo)
      except :
        update.message.reply_text("잘못된 입력입니다.")
        return

      if groupNo < numberOfGroup :
        groupID_URL = '/' + str(groupList[groupNo])
        groupName = groupDict[groupList[groupNo]]['gname']

        self.DB.delete(userID, URL.USER + userID_URL + URL.GROUP + groupID_URL)
        update.message.reply_html("<b>" + groupName + "</b> 그룹을 삭제했습니다.")
        self.log.info(userID, "그룹 삭제 : " + str(groupID))
      else :
        update.message.reply_text("유효하지 않은 번호입니다.")
