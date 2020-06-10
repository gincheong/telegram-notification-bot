import firebase_admin
from firebase_admin import db
from firebase_admin import credentials

class DatabaseControl :
  def __init__(self, credPath, databaseUrl, Log) :
    self.log = Log
    try :
      cred = credentials.Certificate(credPath)
      app = firebase_admin.initialize_app(cred, { 'databaseURL' : databaseUrl } )
    except Exception as e :
      Log.error("000", "[Firebase] DB 초기 연결 // " + str(e))

  def set(self, userId, url, value) :
    try :
      db.reference(url).set(value)
    except Exception as e :
      self.log.error(userId, "[Firebase] Set 오류, " + value + " // " + str(e))

  def get(self, userId, url, shallow=False) :
    # shallow True 설정 시 child 데이터를 가져오지 않음
    try :
      return db.reference(url).get(shallow=shallow)
    except Exception as e :
      self.log.error(userId, "[Firebase] Get 오류 // " + str(e))
      return None
    
  def push(self, userId, url, value) :
    try :
      db.reference(url).push(value)
    except Exception as e :
      self.log.error(userId, "[Firebase] Push 오류, " + value + " // " + str(e))

  def update(self, userId, url, value) : # value = dictionary
    try :
      db.reference(url).update(value)
    except Exception as e :
      self.log.error(userId, "[Firebase] Update 오류, " + value + " // " + str(e))

  def delete(self, userId, url) :
    try :
      db.reference(url).delete()
    except Exception as e :
      self.log.error(userId, "[Firebase] Delete 오류 // " + str(e))