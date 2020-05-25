import telegram
import os
# import multiprocessing
# from functools import partial
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import traceback

import log
import DatabaseControl
from constants import Command as CMD
from constants import FirebaseURL as URL
from constants import Message as MSG
from constants import Bool as B

class Keyword :
  def __init__(self, DB, log) :
    self.DB = DB
    self.log = log

  def isPrivateMsg(self, update) :
    if update.message.chat['type'] == 'private' :
      # 봇에게 직접 메세지를 보낼 때
      return True
    else :
      return False

  def getFullname(self, update) : # 한국처럼 성이 앞으로 간다
    try :
      fullName = update.message.from_user['last_name'] + " " + update.message.from_user['first_name']
    except : # last name을 등록 안 하는 경우
      fullName = update.message.from_user['first_name']

    return fullName

  def keywordAdd(self, bot, update) :
    if self.isPrivateMsg(update) == False :
      # 개인 메세지가 아니면 실행안함
      return

    userID = update.message.chat['id']
    userID_URL = '/' + str(userID)
    userInput = update.message.text

    if userInput == ("/" + CMD.KADD) :
      update.message.reply_text("추가할 키워드를 입력해주세요.\n" + \
        "ex> /kadd 안녕 (\"안녕\" 키워드 추가)")
        # 사용법 보여줌
    else :
      # 1124 new code
      newKeyword = userInput[len(CMD.KADD) + 2 : ].strip().lower() # 소문자 변환하여 등록
      KeywordDict = self.DB.get(userID, URL.USER + userID_URL + URL.KEYWORD)

      if KeywordDict == None or newKeyword not in KeywordDict.values() :
        # 1. 키워드가 하나도 등록되어 있지 않거나 (최초등록)
        # 2. 키워드가 있지만, 중복 데이터가 아닌 경우에
        self.DB.push(userID, URL.USER + '/' + str(userID) + URL.KEYWORD, newKeyword)
        # 키워드 등록

        self.log.info(userID, "키워드 추가 : " + newKeyword)
        update.message.reply_text(newKeyword + " 키워드를 추가했습니다.")
      else :
        # 키워드가 중복되는 경우
        update.message.reply_text("이미 등록된 키워드입니다.")

  def keywordDelete(self, bot, update) :
    if self.isPrivateMsg(update) == False :
      return

    userID = update.message.chat['id']
    userID_URL = '/' + str(userID)
    userInput = update.message.text

    if userInput == ('/' + CMD.KDELETE) :
      update.message.reply_text("삭제할 키워드를 입력하세요.\n" + \
        "ex> /kdel 안녕 (\"안녕\" 키워드 삭제)")
    else :
      # 1124 new code
      # fix : 삭제 시에도 대소문자 구분하지 않게 함(lower() 추가)
      deleteKeyword = userInput[len(CMD.KDELETE) + 2 : ].strip().lower()
      KeywordDict = self.DB.get(userID, URL.USER + userID_URL + URL.KEYWORD)

      if KeywordDict == None :
        # 등록된 키워드가 하나도 없는 경우
        update.message.reply_text("등록된 키워드가 없습니다.")
      elif deleteKeyword not in KeywordDict.values() :
        # 등록되지 않은 키워드를 삭제하려 한 경우
        update.message.reply_text("등록되지 않은 키워드입니다.")
      else :
        # 키워드가 있는 경우, 해당 데이터 key값을 찾아 삭제함
        for key, value in KeywordDict.items() :
          # key값으로 삭제해야 하기 때문에 items() 사용한다.
          if deleteKeyword == value :
            # 키워드가 발견되면
            self.DB.delete(userID, URL.USER + userID_URL + URL.KEYWORD + '/' + key)
            # 해당 key값 이용하여 데이터 삭제 후
            break # 반복문 탈출
        
        # 키워드 삭제 후 메시지 전송
        update.message.reply_text(deleteKeyword + " 키워드를 삭제했습니다.")
        self.log.info(userID, "키워드 삭제 : " + deleteKeyword)


  def keywordList(self, bot, update) :
    if self.isPrivateMsg(update) == False :
      return

    userID = update.message.chat['id']
    userID_URL = '/' + str(userID)

    keywordDict = self.DB.get(userID, URL.USER + userID_URL + URL.KEYWORD)

    try :
      update.message.reply_text("등록된 키워드 목록입니다.\n" + \
             ", ".join(keywordDict.values()))
    except :
      update.message.reply_text("등록된 키워드가 없습니다.")

  def checkMessage(self, bot, update) :
    if self.isPrivateMsg(update) == True :
      return
      # 개인 메세지로 온 것은 무시함
`
    message = update.message.text
    messageID = str(update.message.message_id)
    senderID = str(update.message.from_user['id'])
    senderName = self.getFullname(update)
    groupID = str(update.message.chat['id'])
    groupName = update.message.chat['title']

    groupUserDict = self.DB.get('CheckMessage', URL.GROUP + '/' + groupID + URL.USER)
    # 해당 그룹에 속한 사용자 아이디를 가져온다
    
    # need test
    if groupUserDict == None :
      # 그룹에 등록된 사용자가 없는 경우 혹은
      # 그룹 자체가 등록되어있지 않은 경우 (/start로 등록조차 하지 않음)
      return # 함수 종료

    # 그룹이 있는 경우
    for groupUserID in groupUserDict.values() :
      # 그룹 안에 있는 사용자들을 대상으로..

      if groupUserID == senderID :
        # 자기 자신의 데이터는 보지 않는다.
        continue

      each_userKeyword = self.DB.get('CheckMessage', URL.USER + '/' + str(groupUserID) + URL.KEYWORD)
      # 해당 사용자의 키워드 데이터를 가져온다.

      if each_userKeyword == None :
        # 사용자가 등록한 키워드가 없는 경우
        pass # 다음 사용자
      else :
        # 키워드가 있으면
        for keyword in each_userKeyword.values() :
          # 키워드를 하나씩 가져와서..

          if keyword in message.lower() :
            # 키워드가 메세지에서 발견되었다면
            notiMessage = "%s 님이 호출했습니다.\n그룹 이름 : %s\n메세지 내용 : %s" % (senderName, groupName, message)
            logMessage = "알림 전송 : uid %s / gid %s / mid %s" % (senderID, groupID, messageID)

            self.log.info(groupUserID, "알림 전송 시도") # will be deprecated
            
            try :
              bot.send_message(groupUserID, notiMessage, disable_web_page_preview=True)
              # 링크 미리보기 비활성화
              self.log.info(groupUserID, logMessage)
            except Exception as e:
              self.log.error(groupUserID, "알림 전송 실패")
              self.log.error(groupUserID, str(e))
            # 알림을 전송함

            # 그룹이름이 바뀌었을 경우도 있으니, 그런 경우 데이터 갱신을 해 준다
            savedGroupName = self.DB.get('CheckMessage', URL.GROUP + '/' + groupID + URL.INFO)['groupname']
            if groupName is not savedGroupName :
              # 이름이 갱신된 경우!
              self.DB.update(groupUserID, URL.GROUP + '/' + groupID + URL.INFO, { 'groupname' : groupName })
              # 새 데이터로 update해줌

            # 알림 전송 시 할 작업 끝
            break # 한 사용자의 키워드가 두 개 이상 사용되어도, 한 번만 알람 발생하게 break함