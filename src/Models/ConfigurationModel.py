import JsonModel

class ConfigurationModel(JsonModel.JsonModel):
    def __init__(self):
        self.bot_name = None
        self.bot_token = None
        self.bot_alias = None
        self.bot_logging_channel = None

    def ParseDict(self,obj):
        self.bot_name = obj["bot_name"]
        self.bot_token = obj["bot_token"]
        self.bot_alias = obj["bot_alias"] if "bot_alias" in obj  else "ss"
        self.bot_logging_channel = obj["bot_logging_channel"] if "bot_logging_channel" in obj  else None

    @classmethod
    def Parse(cls,obj):
        cmdObj = cls()
        cmdObj.DoParse(obj)
        return cmdObj

    def GetName(self):
        return self.bot_name
    
    def GetToken(self):
        return self.bot_token

    def GetAlias(self):
        return self.bot_alias

    def GetLoggingChannel(self):
        return self.bot_logging_channel
# import json
# jsonString = '{"bot_name":"botname", "bot_token":"bottoken", "bot_alias":"ss","bot_logging_channel":"botlogging"}'
# x = ConfigurationModel.Parse(jsonString)
# print(str(x))
# print json.dumps(x.__dict__)