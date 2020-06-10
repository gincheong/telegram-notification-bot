from functions import BaseFunction, KeywordFunction, GroupFunction

class Functions :
    def __init__(self, config, database, logger) :
        self.base = BaseFunction.BaseFunction(config, database, logger)
        self.keyword = KeywordFunction.KeywordFunction(config, database, logger)
        self.group = GroupFunction.GroupFunction(config, database, logger)