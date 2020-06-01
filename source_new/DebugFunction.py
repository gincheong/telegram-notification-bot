import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

class DebugFunction :
    def __init__(self) :
        pass

    def getMessageData(self, update, context) :
        print(update.message)