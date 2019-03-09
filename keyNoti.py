import telegram
import os
import firebase_admin
from firebase_admin import credentials
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from firebase import firebase

import log
from constants import Command as CMD
from constants import Firebase as FB
from constants import Message as MSG

# /setprivacy DISABLED # 명령이 아닌 그룹 메세지에도 반응

class keyNotiBot :
  def __init__(self) :
    ###############################################
    self.token = <BOT_TOKEN>
    self.firebase = firebase.FirebaseApplication(<FIREBASE_URL>, None)

    # cred = credentials.Certificate('/PATH/TO/KEY.json')
    # app = firebase_admin.initialize_app(cred)
    # SDK 활성화

    ###############################################

    self.core = telegram.Bot(self.token)
    self.updater = Updater(self.token)

    self.keywordInput = False
    self.readMessage = True
    self.keywordDic = {}

    self.log = log.Log()
    self.log.info("000", "Program Start")
    # 로그 기록

  def isPrivateMsg(self, update) :
    if update.message.chat['type'] == 'private' :
      # 봇에게 직접 메세지를 보낼 때
      return True
    else :
      return False

  def isMyMsg(self, update) :
    if update.message.from_user['id'] == self.userId :
      return True
    else :
      return False

  def msgHandler(self, func) :
    self.updater.dispatcher.add_handler(MessageHandler(Filters.text, func))
  def cmdHandler(self, cmd, func) :
    self.updater.dispatcher.add_handler(CommandHandler(cmd, func))
  
  def initHandler(self) :
    self.cmdHandler(CMD.KEYWORD, self.addKeyword)
    self.cmdHandler(CMD.HELP, self.cmdHelp)
    self.cmdHandler(CMD.LIST, self.showList)
    self.cmdHandler(CMD.DELETE, self.deleteKeyword)
    self.cmdHandler(CMD.INFO, self.showInfo)

    self.msgHandler(self.getMessage) # 메세지가 있을 때마다 호출됨

    self.cmdHandler('debug', self.debug)

  def debug(self, bot, update) :
    print(update.message)

  def boot(self) :
    self.log.info("000", "Bot Start")
    self.cmdHandler(CMD.START, self.start)

    self.updater.start_polling()
    self.updater.idle()
  
  def start(self, bot, update) :
    if self.isPrivateMsg(update) == False :
      # 개인 메세지로 보낸 명령어가 아니면 실행 안함
      return

    self.userId = update.message.chat['id']
    self.log.info(self.userId, "Start 명령어를 읽었습니다.")
    self.log.warn(self.userId, str(update.message))
    update.message.reply_html(MSG.WELCOME)
    update.message.reply_html(MSG.PREVIEW)
    self.initHandler()
    # 명령어를 활성화시킨다.

    # firebase에서 키워드를 가져온다
    try :
      keywords = self.firebase.get(FB.KEYWORD, str(self.userId))
    except Exception as e :
      self.log.error(self.userId, "[Firebase] Start시 키워드 가져오기 : " + str(e))
      update.message.reply_text("오류가 발생했습니다.")

    if keywords == None :
      self.log.info(self.userId, "저장된 키워드 없음")
      self.keywordDic[self.userId] = list()
    else :
      self.keywordDic[self.userId] = keywords
      self.log.info(self.userId, "저장된 키워드 읽어오기 성공 : " + ", ".join(self.keywordDic[self.userId]))

  # userFunc
  def cmdHelp(self, bot, update) :
    if self.isPrivateMsg(update) == False :
      # 개인 메세지가 아니면 실행안함
      return
    update.message.reply_text(MSG.CMDLIST)

  # 그룹 메세지를 읽어서 키워드를 확인하는 함수
  def getMessage(self, bot, update) :
    # 자기 자신의 메세지에는 호출 반응 하지 않는다
    if self.isMyMsg(update) :
      return

    if self.readMessage == True and self.isPrivateMsg(update) == False :
      # 메세지를 읽어도 되는 상황이면 (명령어 인식 중이 아님)
      # + 봇에게 보낸 메세지가 아니면

      received = update.message.text

      # D.B 접속
      
      for item in self.keywordDic[self.userId] :  
        if item in received :
          # 호출 단어가 사용되었는가 확인 
          senderName = ""

          if update.message.from_user['last_name'] != None :
            senderName = update.message.from_user['last_name'] + " "
          senderName += update.message.from_user['first_name']
          groupName = update.message.chat['title']
          
          notiMsg = senderName + " 님이 호출했습니다.\n" + \
            "그룹 이름 : " + groupName + "\n" + \
            "메세지 내용 : " + update.message.text

          self.core.send_message(chat_id=self.userId, text=notiMsg)
          self.log.info(self.userId, "알람 전송 : " + senderName + ", " + groupName + ", " + update.message.text)
          
          break # 호출 단어가 두 개 이상 사용되어도, 한 번만 알린다.

  def addKeyword(self, bot, update) :
    if self.isPrivateMsg(update) == False :
      # 개인 메세지가 아니면 실행안함
      return

    self.readMessage = False # 명령어 입력을 위해 메세지 읽기 중단
    userInput = update.message.text

    if userInput == ("/" + CMD.KEYWORD) : # 아무 키워드로 입력하지 않음
      update.message.reply_text("추가할 키워드를 입력해주세요.\n" + \
        "ex> /keyword 안녕 (\"안녕\" 키워드 추가)")
          # 사용법 보여줌
    else :
      newKeyword = userInput[9 : ] # 사용자 입력에서 키워드 따오기
      if self.keywordDic[self.userId] is not None : 
        if newKeyword in self.keywordDic[self.userId] :
          update.message.reply_text("이미 등록된 키워드입니다.")
        else :
          self.keywordDic[self.userId].append(str(newKeyword))
          update.message.reply_text('"' + str(newKeyword) + '"' + " 키워드를 추가했습니다.")
          self.log.info(self.userId, "새 키워드 추가 : " + str(newKeyword))

          try :
            self.firebase.put(FB.KEYWORD, str(self.userId), self.keywordDic[self.userId])
          except Exception as e :
            self.log.error(self.userId, "[Firebase] 새 키워드 추가 : " + str(e))
            update.message.reply_text("오류가 발생했습니다.")
      else : # None이면 기존에 저장된 키워드가 없는 것
        self.keywordDic[self.userId] = str(newKeyword)
        update.message.reply_text('"' + str(newKeyword) + '"' + " 키워드를 추가했습니다.")
        self.log.info(self.userId, "새 키워드 추가 : " + str(newKeyword))

        try :
          self.firebase.put(FB.KEYWORD, str(self.userId), self.keywordDic[self.userId])
        except Exception as e :
          self.log.error(self.userId, "[Firebase] 새 키워드 추가 : " + str(e))
          update.message.reply_text("오류가 발생했습니다.")

    self.readMessage = True

  def showList(self, bot, update) :
    if self.isPrivateMsg(update) == False :
      return

    update.message.reply_text("등록된 키워드 목록을 확인합니다.")

    listToString = str()
    if self.keywordDic[self.userId] is not None :
      for each in self.keywordDic[self.userId] :
        listToString += '"' + each + '" '
      update.message.reply_text(listToString)
      self.log.info("현재 키워드 목록 확인 : " + listToString)
    else :
      update.message.reply_text("등록된 키워드가 없습니다.")
  
  def deleteKeyword(self, bot, update) :
    if self.isPrivateMsg(update) == False :
      return

    self.readMessage = False
    userInput = update.message.text

    if userInput == ("/" + CMD.DELETE) :
      update.message.reply_text("삭제할 키워드를 입력하세요.\n" + \
        "ex> /delete 안녕 (\"안녕\" 키워드 삭제)")
    else :
      deleteTarget = userInput[8 : ]
      if self.keywordDic[self.userId] is not None :
        if deleteTarget in self.keywordDic[self.userId] :
          self.keywordDic[self.userId].remove(deleteTarget)
          update.message.reply_text("삭제되었습니다.")

          try :
            self.firebase.put(FB.KEYWORD, str(self.userId), self.keywordDic[self.userId])
          except Exception as e :
            self.log.error(self.userId, "[Firebase] 키워드 삭제 : " + str(e))
            update.message.reply_text("오류가 발생했습니다.")
          
          self.log.info(self.userId, "키워드 삭제 : " + deleteTarget)
        else :
          self.log.info(self.userId, "키워드 삭제 실패")
          update.message.reply_text("등록되지 않은 키워드입니다.")
      else : # None이면 키워드 없는 상태
        update.message.reply_text("등록된 키워드가 없습니다.")
        self.log.warn("등록된 키워드 없는 상태에서 삭제 시도")
    
    self.readMessage = True

  def showInfo(self, bot, update) :
    if self.isPrivateMsg(update) == False :
      return
    
    update.message.reply_text("개발중인 봇입니다.")
    update.message.reply_html(MSG.INFO, disable_web_page_preview=True)

if __name__ == "__main__":
    knoti = keyNotiBot()
    knoti.boot()
