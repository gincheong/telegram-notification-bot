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
    userInput = update.message.text

    if userInput == ("/" + CMD.KADD) :
      update.message.reply_text("추가할 키워드를 입력해주세요.\n" + \
        "ex> /kadd 안녕 (\"안녕\" 키워드 추가)")
        # 사용법 보여줌
    else :
      newKeyword = userInput[len(CMD.KADD) + 2 : ].strip().lower()
      keywordDict = self.DB.get(userID, URL.USER + '/' + str(userID) + URL.KEYWORD)
      
      if keywordDict == None or newKeyword not in keywordDict.values() :
        self.DB.push(userID, URL.USER + '/' + str(userID) + URL.KEYWORD, newKeyword)

        self.log.info(userID, "키워드 추가 : " + newKeyword)
        update.message.reply_html("<b>" + newKeyword + "</b> 키워드를 추가했습니다.")
      else :
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
      deleteKeyword = userInput[len(CMD.KDELETE) + 2 : ].strip()
      keywordDict = self.DB.get(userID, URL.USER + userID_URL + URL.KEYWORD)
      
      if keywordDict == None :
        update.message.reply_text("등록된 키워드가 없습니다.")
      elif deleteKeyword not in keywordDict.values() :
        update.message.reply_text("등록되지 않은 키워드입니다.")
      else :
        for key, value in keywordDict.items() :
          if deleteKeyword == value :
            self.DB.delete(userID, URL.USER + userID_URL + URL.KEYWORD + '/' + key)
            break
        
        update.message.reply_html("<b>" + deleteKeyword + "</b> 키워드를 삭제했습니다.")
        self.log.info(userID, "키워드 삭제 : " + deleteKeyword)

  def keywordList(self, bot, update) :
    if self.isPrivateMsg(update) == False :
      return

    userID = update.message.chat['id']
    userID_URL = '/' + str(userID)

    keywordDict = self.DB.get(userID, URL.USER + userID_URL + URL.KEYWORD)

    try :
      update.message.reply_html("등록된 키워드 목록입니다.\n" + \
            "<b>" + ", ".join(keywordDict.values()) + "</b>")
    except :
      update.message.reply_text("등록된 키워드가 없습니다.")

  def keywordFind(self, bot, messageData, allUserData) :

    for uid, udata in allUserData.items() :
      try :
        notificationState = udata['config']['notification']
        # 그룹에 /start 하지 않으면 'config'가 정의되지 않는데
        # 그 부분을 수정해야 함, 지금은 임시로 except로 뺀 상태
        # 아니면 굳이 오류처리 안 해도 될ㄹ 것도 같고
      except :
        continue

      if (uid == messageData['senderID']) or (notificationState == B.OFF) :
        continue # 당사자이거나, 알람이 꺼진 사용자 스킵

      try :
        kList = list(udata['keyword'].values())
        gDict = udata['group'].items()
      except :
        continue
        # 키워드 등록을 안 한 사용자

      for item in gDict :
        gid, gdata = item
        # 사용자 DB에 저장된 그룹 데이터

        if (gid == messageData['groupID']) and gdata['alarm'] == B.ON :
          # 2. 그룹에 속한 유저 검색
          # 3. 그룹 알림을 켰는지 확인

          for kvalue in kList :
            if kvalue in messageData['text'].lower() :
              # 4. 키워드 사용 확인

              notiMessage = "<i>%s</i> 님이 호출했습니다.\n그룹 이름 : <i>%s</i>\n메세지 내용 : <i>%s</i>" % (messageData['senderName'], messageData['groupName'], messageData['text'])
              
              self.log.info(uid, "알림 전송 시도")
              bot.send_message(uid, notiMessage, parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)
              self.log.info(uid, "알림 전송 : " + messageData['senderID'] + '/' + messageData['senderName'] + '/' + messageData['groupID'] + '/' + messageData['groupName'] + '/' + messageData['text'])

              if messageData['groupName'] is not gdata['gname'] :
                # 그룹 이름을 못 찾는다 -> 그룹명이 바뀌었는데 갱신 안됨
                self.DB.update(uid, URL.USER + '/' + str(uid) + URL.GROUP + '/' + str(gid), { 'gname' : messageData['groupName'] }) # 갱신함

              break # 동일 사용자의 키워드가 여러 번 사용돼도 한 번만 알림

  def checkMessage(self, bot, update) :
    if self.isPrivateMsg(update) == True :
      return
      # 개인 메세지로 온 것은 무시함

    messageData = dict()
    messageData['text'] = update.message.text
    messageData['senderID'] = str(update.message.from_user['id'])
    messageData['groupID'] = str(update.message.chat['id']) # 어느 그룹인지 체크
    messageData['groupName'] = update.message.chat['title']
    messageData['senderName'] = self.getFullname(update)

    allUserData = self.DB.get('CHECKMESSAGE', URL.USER)

    self.keywordFind(bot, messageData, allUserData)