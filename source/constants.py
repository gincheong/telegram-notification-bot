class Bool :
  ON = 1
  OFF = 0

class Command :
  KDELETE = "kdel"
  KADD = "kadd"
  KLIST = "klist"

  GDELETE = "gdel"
  GTOGGLE = "gtoggle"
  GLIST = "glist"

  HELP = "help"
  INFO = "info"
  START = "start"
  HOWTO = "howto"
  DISABLE = "disable"
  ENABLE = "enable"

class FirebaseURL :
  KEYWORD = "/keyword"
  CONFIG = "/config"
  GROUP = "/group"
  USER  = "/user"

class Message :
  WELCOME = "원하는 그룹에 봇을 초대하고, 그룹 내 채팅으로 봇에게 /start 명령어를 입력하세요.\n" + \
            "/howto 로 사용 방법, /help 로 사용 가능한 명령어 목록을 볼 수 있습니다.\n" + \
            "/info 명령어로 정보를 확인할 수 있습니다."

  PREVIEW = '<i>' + \
            "EX> 키워드에 '밥' 을 등록한 경우\n" + \
            "홍 길동 님이 호출했습니다.\n" + \
            "그룹 이름 : XX대학교 동기 그룹\n" + \
            "메세지 내용 : 밥 먹으러 갈 사람?" + \
            '</i>'

  CMDLIST = "/kadd <키워드> : 알람을 받을 키워드를 설정합니다.\n" + \
            "/kdel <키워드> : 등록된 키워드를 삭제합니다.\n" + \
            "/klist : 설정한 키워드 목록을 확인합니다.\n" + \
            "\n" + \
            "/glist : 사용자에게 등록된 그룹 목록을 확인합니다.\n" + \
            "/gtoggle <번호> : 그룹별로 키워드 알림을 ON/OFF 합니다.\n" + \
            "/gdel <번호> : 이미 등록된 그룹을 삭제합니다.\n" + \
            "\n" + \
            "/enable, /disable : 봇 전체 알림을 ON/OFF 합니다.\n" + \
            "/info : 봇 정보를 확인합니다.\n" + \
            "/howto : 봇 사용 방법을 확인합니다."

  HOWTO = "카카오톡의 키워드 알림 기능을 본따 만들었습니다.\n" + \
          "1. 키워드 알림을 활성화할 그룹 채팅에 봇을 초대합니다.\n" + \
          "2. <b>그룹 내 채팅으로</b> 봇에게 /start 명령어를 입력해 그룹 알림을 활성화합니다.\n" + \
          "3. <b>봇과의 개인 대화로</b> 키워드를 등록합니다."

  INFO = "2019년 3월 29일부터 AWS에서 실행되고 있습니다.\n" + \
          "데이터는 Google Firebase에 저장합니다.\n" + \
          "키워드 데이터는 암호화하지 않고 저장하므로 개인정보를 입력하지 마세요.\n" + \
          "알림 기능을 위해 봇이 그룹 채팅의 메시지에 접근 권한을 가지고 있습니다.\n" + \
          'Github : <a href="https://github.com/gincheong/telegram-notification-bot">telegram-notification-bot</a>\n' + \
          "Telegram : @gincheong\n" + \
          "2019.03.29"

  UPDATELOG = ""