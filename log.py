import time

class Log :
  def __init__(self) :
    now = time.localtime()
    filename = "%04d%02d%02d" % (now.tm_year, now.tm_mon, now.tm_mday)
    self.f = open("log/" + filename + ".txt", 'a', encoding='utf-8')

  def updateTimeStamp(self) :
    now = time.localtime()
    self.timestamp = "\n[%04d-%02d-%02d %02d:%02d:%02d]" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

  def info(self, uid, text) :
    self.updateTimeStamp()
    self.f.write(self .timestamp + " [INFO] (" + str(uid) + ") " + str(text))
    self.f.flush()

  def warn(self, uid, text) :
    self.updateTimeStamp()
    self.f.write(self.timestamp + " [WARN] (" + str(uid) + ") " + str(text))
    self.f.flush()

  def error(self, uid, text) :
    self.updateTimeStamp()
    self.f.write(self.timestamp + " [ERROR] (" + str(uid) + ") " + str(text))
    self.f.flush()