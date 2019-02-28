import telegram
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import log
from constants import Commands as CMD

# /setprivacy DISABLED # 명령이 아닌 그룹 메세지에도 반응

class keyNotiBot :
  def __init__(self) :
    ###############################################
    self.token = <BOT_TOKEN>
    ###############################################

    self.core = telegram.Bot(self.token)
    self.updater = Updater(self.token)

    self.keywordInput = False
    self.readMessage = True
    self.keywordDic = {}


    self.log = log.Log()
    self.log.info("Program Start")
    # 로그 기록

    self.chatLog = open("chatlog", mode="a+t", encoding="utf-8")

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
  def sendMessage(self, text) :
    self.core.send_message(chat_id=self.userId, text=text)
  
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
    self.log.info("Bot Start")
    self.cmdHandler(CMD.START, self.start)

    self.updater.start_polling()
    self.updater.idle()
  
  def start(self, bot, update) :
    if self.isPrivateMsg(update) == False :
      # 개인 메세지로 보낸 명령어가 아니면 실행 안함
      return
    self.log.info("Start 명령어를 읽었습니다.")
    update.message.reply_text("봇을 시작합니다.")
    update.message.reply_text("명령어가 활성화되었습니다. /help 명령어로 사용 가능한 명령어 목록을 볼 수 있습니다.")
    self.initHandler()
    # 명령어를 활성화시킨다.

    # DB로 가서 기존 데이터가 있는지 확인
    # 지금은 대충 파일로 대체

    self.userId = update.message.chat['id']
    self.f = open(str(self.userId), 'a+t', encoding='utf-8')
    # 텍스트 읽기+쓰기 모드, 기존 파일 내용 보존
    self.keywordDic[self.userId] = list()
    self.f.seek(0, os.SEEK_SET)
    for each in self.f :
      self.keywordDic[self.userId].append(each.strip()) # \n 개행문자를 제거하고 읽어옴
    self.log.info("저장된 키워드 읽어오기 성공, " + ", ".join(self.keywordDic[self.userId]))
  

  # userFunc
  def cmdHelp(self, bot, update) :
    if self.isPrivateMsg(update) == False :
      # 개인 메세지가 아니면 실행안함
      return
    update.message.reply_text("/keyword <...> : 알람을 받을 키워드를 설정합니다.\n" + \
      "/delete <...> : 등록된 키워드를 삭제합니다.\n" + \
      "/list : 설정한 키워드 목록을 확인합니다.\n" + \
      "/info : 봇 정보를 확인합니다.")

  def getMessage(self, bot, update) :
    if self.isMyMsg(update) :
      return
      # 내가 보내는 메세지면 더 읽을 필요 없다

    # self.chatLog.writelines(str(update.message) + "\n")
    # self.chatLog.flush()

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
          self.log.info("send notiMsg : " + senderName + ", " + groupName + ", " + update.message.text)
          
          break # 호출 단어가 두 개 이상 사용되어도, 한 번만 알린다.

  def addKeyword(self, bot, update) :
    if self.isPrivateMsg(update) == False :
      # 개인 메세지가 아니면 실행안함
      return

    self.readMessage = False # 명령어 입력을 위해 메세지 읽기 중단
    userInput = update.message.text

    if userInput == ("/" + CMD.KEYWORD) : # 아무 키워드로 입력하지 않음
      self.sendMessage("추가할 키워드를 입력해주세요.\n" + \
        "ex> /keyword 안녕 (\"안녕\" 키워드 추가)")
          # 사용법 보여줌
    else :
      newKeyword = userInput[9 : ]
      if newKeyword in self.keywordDic[self.userId] :
        self.sendMessage("이미 등록된 키워드입니다.")
      else :
        self.keywordDic[self.userId].append(str(newKeyword))
        self.sendMessage('"' + str(newKeyword) + '"' + " 키워드를 추가했습니다.")
        self.log.info("new keyword added : " + str(newKeyword))

        self.f.writelines(str(newKeyword) + "\n")
        self.f.flush()

    self.readMessage = True

  def showList(self, bot, update) :
    if self.isPrivateMsg(update) == False :
      return

    self.sendMessage("등록된 키워드 목록입니다.")

    listToString = ""
    for each in self.keywordDic[self.userId] :
      listToString += '"' + each + '" '

    self.sendMessage(listToString)
    self.log.info("current keyword list : " + listToString)
  
  def deleteKeyword(self, bot, update) :
    if self.isPrivateMsg(update) == False :
      return

    self.readMessage = False
    userInput = update.message.text

    if userInput == ("/" + CMD.DELETE) :
      self.sendMessage("삭제할 키워드를 입력하세요.\n" + \
        "ex> /delete 안녕 (\"안녕\" 키워드 삭제)")
    else :
      deleteTarget = userInput[8 : ]
      if deleteTarget in self.keywordDic[self.userId] :
        self.keywordDic[self.userId].remove(deleteTarget)
        self.sendMessage("삭제되었습니다.")

        self.f.seek(0, os.SEEK_SET)
        # 파일에서 삭제하기


        self.log.info("keyword deleted : " + deleteTarget)
      else :
        self.sendMessage("등록되지 않은 키워드입니다.")
    
    self.readMessage = True

  def showInfo(self, bot, update) :
    if self.isPrivateMsg(update) == False :
      return
    
    update.message.reply_text("개발중인 봇입니다.")
    update.message.reply_text("카카오톡처럼 키워드 알림 쓰고시퍼용")

if __name__ == "__main__":
    knoti = keyNotiBot()
    knoti.boot()