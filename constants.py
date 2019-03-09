class Command :
  DELETE = "delete"
  KEYWORD = "keyword"
  HELP = "help"
  LIST = "list"
  INFO = "info"
  START = "start"

class Firebase :
  KEYWORD = "/keywords"

class Message :
  WELCOME = "봇을 시작합니다.\n" + \
            "사용자가 등록한 키워드가 사용되면 봇이 메세지를 보내 알립니다.\n" + \
            "/help 로 사용 가능한 명령어 목록을 볼 수 있습니다.\n"
  PREVIEW = '<i>' + \
            "EX>\n" + \
            "홍 길동 님이 호출했습니다.\n" + \
            "그룹 이름 : 율도국\n" + \
            "메세지 내용 : 안녕하세요" + \
            '</i>'
  CMDLIST = "/keyword <...> : 알람을 받을 키워드를 설정합니다.\n" + \
            "/delete <...> : 등록된 키워드를 삭제합니다.\n" + \
            "/list : 설정한 키워드 목록을 확인합니다.\n" + \
            "/info : 봇 정보를 확인합니다."

  INFO = "서버가 없어서 비정기적으로 실행중입니다.\n" + \
            "키워드는 구글 Firebase에 저장하고 있습니다.\n" + \
            "현재 DB는 공개되어 있습니다. 개인정보를 입력하지 마세요.\n" + \
            "봇을 그룹 내에 참여시켜야만 작동하며, 그룹 내의 모든 채팅을 봇이 읽습니다.\n" + \
            "키워드 알람이 발생한 대화를 제외한 어떤 대화 내용도 기록하지 않습니다.\n" + \
            'Github : <a href="https://github.com/gincheong/telegram-notification-bot">gincheong</a>'