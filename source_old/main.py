import keyNoti

if __name__ == "__main__":

  bot_token = <BOT_TOKEN>
  serviceAccountKey = <PATH/TO/KEY>
  firebaseURL = <FIREBASE_URL>

  keyNoti.keyNotiBot(bot_token, serviceAccountKey, firebaseURL).boot()