import time

class Log :
  def __init__(self) :
    pass

  def openFile(self, localtime) :
    filename = "%04d%02d%02d" % (localtime.tm_year, localtime.tm_mon, localtime.tm_mday)
    
    return open("log/" + filename + ".txt", 'a', encoding='utf-8')

  def updateTimeStamp(self) :
    now = time.localtime()
    self.timestamp = "\n[%04d-%02d-%02d %02d:%02d:%02d]" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    
    return now

  def info(self, uid, text) :
    log = self.openFile(self.updateTimeStamp())
    log.write(self .timestamp + " [INFO] (" + str(uid) + ") " + str(text))
    log.flush()
    log.close()

  def warn(self, uid, text) :
    log = self.openFile(self.updateTimeStamp())
    log.write(self.timestamp + " [WARN] (" + str(uid) + ") " + str(text))
    log.flush()
    log.close()

  def error(self, uid, text) :
    log = self.openFile(self.updateTimeStamp())
    log.write(self.timestamp + " [ERROR] (" + str(uid) + ") " + str(text))
    log.flush()
    log.close()