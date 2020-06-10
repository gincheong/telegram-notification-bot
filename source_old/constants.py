class Bool :
  ON = 1
  OFF = 0

class Command :
  KDELETE = "kdel"
  KADD = "kadd"
  KLIST = "klist"

  GLIST = "glist"

  HELP = "help"
  INFO = "info"
  START = "start"
  GDELETE = "delete"
  HOWTO = "howto"

class FirebaseURL :
  KEYWORD = "/keyword"
  # CONFIG = "/config" # will be deprecated
  INFO = "/info"
  GROUP = "/group"
  USER  = "/user"
  REGISTERED_GROUP = '/registered_group'

class Message :
  WELCOME = "원하는 그룹에 봇을 초대하고, 그룹 내 채팅으로 봇에게 /start 명령어를 입력하세요.\n" + \
            "/howto 로 사용 방법, /help 로 사용 가능한 명령어 목록을 볼 수 있습니다.\n"

  PREVIEW = '<i>' + \
            "EX> 키워드에 '밥' 을 등록한 경우\n" + \
            "홍 길동 님이 호출했습니다.\n" + \
            "그룹 이름 : XX대학교 동기 그룹\n" + \
            "메세지 내용 : 밥 먹으러 갈 사람?" + \
            '</i>'

  CMDLIST = "/kadd 키워드 : 알람을 받을 키워드를 설정합니다.\n" + \
            "/kdel 키워드 : 등록된 키워드를 삭제합니다.\n" + \
            "/klist : 설정한 키워드 목록을 확인합니다.\n" + \
            "\n" + \
            "/glist : 사용자에게 등록된 그룹 목록을 확인합니다.\n" + \
            "\n" + \
            "/howto : 봇 사용 방법을 확인합니다."

  HOWTO = "카카오톡의 키워드 알림 기능을 본따 만들었습니다.\n" + \
          "1. 키워드 알림을 활성화할 그룹 채팅에 봇을 초대합니다.\n" + \
          "2. <b>그룹 내 채팅으로</b> 봇에게 /start 명령어를 입력해 그룹 알림을 활성화합니다.\n" + \
          "3. <b>봇과의 개인 대화로</b> 키워드를 등록합니다."

  INFO = "키워드 감지를 위해 봇이 메시지 접근 권한을 가지고 있습니다. (Group Privacy Disabled)\n" + \
         "작동 확인을 위하여 텔레그램 내부의 그룹ID, 사용자ID, 메세지ID 를 기록합니다.\n" + \
         "가입 시 입력한 사용자 ID와는 다른 것이며, 해당 ID들로는 사용자 이름, 메세지 내용 등을 알 수 없습니다.\n" + \
         "등록된 그룹을 사용자가 확인할 수 있도록, 그룹명만을 예외적으로 저장하고 있습니다.\n" + \
         "데이터는 암호화하지 않고 저장하므로 중요한 개인정보를 입력하지 마세요.\n" + \
         'Github : <a href="https://github.com/gincheong/telegram-notification-bot">telegram-notification-bot</a>\n' + \
         "Telegram : @gincheong\n" + \
         "2020.05.25" 

  UPDATELOG = ""
