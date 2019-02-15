import telegram
import log
from constants import Commands as CMD
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# /setprivacy DISABLED # 명령이 아닌 그룹 메세지에도 반응

class keyNotiBot :
  def __init__(self) :
    ###############################################
    self.token = <BOT_ID>
    ###############################################

    self.core = telegram.Bot(self.token)
    self.updater = Updater(self.token)

    self.keywordInput = False
    self.readMessage = True
    self.keywordList = []

    self.log = log.Log()
    self.log.info("Program Start")
    # 로그 기록

  def isPrivateMsg(self, update) :
    if update.message.chat['type'] == 'private' and update.message.chat_id == self.id :
      # 개인 메세지로 온 말이면
      return True
    else :
      return False

  def isMyMsg(self, update) :
    if update.message.from_user['id'] == self.id :
      return True
    else :
      return False

  def msgHandler(self, func) :
    self.updater.dispatcher.add_handler(MessageHandler(Filters.text, func))
  def cmdHandler(self, cmd, func) :
    self.updater.dispatcher.add_handler(CommandHandler(cmd, func))

  def initHandler(self) :
    self.msgHandler(self.getMessage)
    
    self.cmdHandler(CMD.KEYWORD, self.addKeyword)
    self.cmdHandler(CMD.HELP, self.cmdHelp)
    self.cmdHandler(CMD.START, self.cmdHelp)
    self.cmdHandler(CMD.LIST, self.showList)
    self.cmdHandler(CMD.DELETE, self.deleteKeyword)
    self.cmdHandler(CMD.INFO, self.showInfo)

    self.cmdHandler('debug', self.debug)

  def debug(self, bot, update) :
    print(update.message)

  def start(self) :
    self.initHandler()
    self.updater.start_polling()
    self.updater.idle()
  
  def sendMessage(self, text) :
    self.core.send_message(chat_id=self.id, text=text)

  # userFunc
  def cmdHelp(self, bot, update) :
    if self.isPrivateMsg(update) == False :
      # 개인 메세지가 아니면 실행안함
      return
    self.sendMessage("/keyword : 알람을 받을 키워드를 설정합니다.")
    self.sendMessage("/list : 설정한 키워드 목록을 확인합니다.")

  def getMessage(self, bot, update) :
    if self.isMyMsg(update) :
      return
      # 내가 보내는 메세지면 더 읽을 필요 없다

    if self.readMessage == True and self.isPrivateMsg(update) == False :
      # 메세지를 읽어도 되는 상황이면 (명령어 인식 중이 아님)
      # + 개인 메세지가 아니면

      received = update.message.text
      for item in self.keywordList :  
        if item in received :
          # 호출 단어가 사용되었는가 확인
          senderName = update.message.from_user['last_name'] + " " + update.message.from_user['first_name']
          groupName = update.message.chat['title']
          
          notiMsg = senderName + " 님이 호출했습니다.\n" + \
            "그룹 이름 : " + groupName + "\n" + \
            "메세지 내용 : " + update.message.text
          # 코드 상의 줄바꿈은 백슬래시로

          self.core.send_message(chat_id=self.id, text=notiMsg)
          self.log.info("send notiMsg : " + senderName + ", " + groupName + ", " + update.message.text)

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
      if newKeyword in self.keywordList :
        self.sendMessage("이미 등록된 키워드입니다.")
      else :
        self.keywordList.append(str(newKeyword))
        self.sendMessage('"' + str(newKeyword) + '"' + " 키워드를 추가했습니다.")
        self.log.info("new keyword added : " + str(newKeyword))
    self.readMessage = True

  def showList(self, bot, update) :
    if self.isPrivateMsg(update) == False :
      return

    self.sendMessage("등록된 키워드 목록입니다.")

    listToString = ""
    for each in self.keywordList :
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
      if deleteTarget in self.keywordList :
        self.keywordList.remove(deleteTarget)
        self.sendMessage("삭제되었습니다.")
        self.log.info("keyword deleted : " + deleteTarget)
      else :
        self.sendMessage("등록되지 않은 키워드입니다.")
    
    self.readMessage = True

  def showInfo(self, bot, update) :
    if self.isPrivateMsg(update) == False :
      return
    
    update.message.reply_text("개발중인 봇입니다.")
    update.message.reply_text("카카오톡의 키워드 알림 쓰고시퍼성")

if __name__ == "__main__":
    knoti = keyNotiBot()
    knoti.start()