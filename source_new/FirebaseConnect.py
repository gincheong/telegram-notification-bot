import firebase_admin
from firebase_admin import db, credentials

from configparser import ConfigParser

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

class FirebaseConnect :
    def __init__(self, configPath) :
        config = ConfigParser()
        config.read(configPath)
        
        FIREBASE_URL = config['FIREBASE']['URL']
        FIREBASE_CERTPATH = config['FIREBASE']['CERTPATH']

        cred = credentials.Certificate(FIREBASE_CERTPATH)
        firebase_admin.initialize_app(cred, { 'databaseURL' : FIREBASE_URL })
    
    def set(self, url, value) :
        db.reference(url).set(value)

    def get(self, url, shallow=False) :
        # shallow=True 시 child 데이터(key-val의 val에 해당)를 True,False로만 가져옴
        return db.reference(url).get(shallow=shallow)
    
    def push(self, url, value) :
        db.reference(url).push(value)
    
    def update(self, url, value) :
        db.reference(url).update(value)

    def delete(self, url) :
        db.reference(url).delete()
    