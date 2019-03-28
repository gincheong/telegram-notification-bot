import telegram
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import log
import DatabaseControl
from constants import Command as CMD
from constants import FirebaseURL as URL
from constants import Message as MSG

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




