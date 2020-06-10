import logging
from logging import handlers
from configparser import ConfigParser

class Logger :
    def __init__(self, config) :
        LOG = config['LOG']

        FILEPATH = LOG['FILEPATH']
        FILENAME = LOG['FILENAME']
        SUFFIX = "%Y%m%d.log"

        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        timedHandler = handlers.TimedRotatingFileHandler(filename=FILEPATH + '/' + FILENAME, when="midnight", interval=1, encoding="utf-8")
        timedHandler.setFormatter(formatter)
        timedHandler.suffix = SUFFIX
        # 기본적으로 tnbLog 파일에 기록했다가, 하루가 지나면 해당 파일에 날짜를 붙여서 새로 저장하고
        # 다시 tnbLog 파일을 생성해서 거기에 오늘자 로그를 기록함

        logger = logging.getLogger()
        logger.setLevel(logging.INFO) # 배포 시 INFO로 되어있는지 확인
        logger.addHandler(timedHandler)
        self.logger = logger

    def getInstance(self) :
        return self.logger