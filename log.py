import time

class Log :
  def __init__(self) :
    now = time.localtime()
    filename = "%04d%02d%02d" % (now.tm_year, now.tm_mon, now.tm_mday)
    self.f = open(filename + ".txt", 'a', encoding='utf-8')

  def updateTimeStamp(self) :
    now = time.localtime()
    self.timestamp = "\n[%04d-%02d-%02d %02d:%02d:%02d]" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

  def info(self, text) :
    self.updateTimeStamp()
    self.f.writelines(self.timestamp + " [INFO] " + text)
    self.f.flush()

  def warn(self, text) :
    self.updateTimeStamp()
    self.f.writelines(self.timestamp + " [WARN] " + text)
    self.f.flush()

  def error(self, text) :
    self.updateTimeStamp()
    self.f.writelines(self.timestamp + " [ERROR] " + text)
    self.f.flush()