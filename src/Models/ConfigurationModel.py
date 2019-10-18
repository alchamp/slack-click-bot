import JsonModel

class ConfigurationModel(JsonModel.JsonModel):
    def __init__(self):
        self.bot_name = None
        self.bot_token = None
        self.bot_alias = None
        self.bot_logging_channel = None
        self.maximize_windows = False

    def ParseDict(self,obj):
        self.bot_name = obj["bot_name"]
        self.bot_token = obj["bot_token"]
        self.bot_alias = obj["bot_alias"] if "bot_alias" in obj  else "ss"
        self.bot_logging_channel = obj["bot_logging_channel"] if "bot_logging_channel" in obj  else None
        maximizeWindowsIn = obj["maximize_windows"] if "maximize_windows" in obj  else False
        if(isinstance(maximizeWindowsIn, basestring)):
            maximizeWindowsIn.decode(encoding='UTF-8',errors='ignore').lower()
            if(maximizeWindowsIn == "true" or maximizeWindowsIn == "y" or maximizeWindowsIn == "yes"):
                self.maximize_windows = True
        else:
             self.maximize_windows = (maximizeWindowsIn == True)

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
    
    def ShouldMaximizeWindows(self):
        return self.maximize_windows

# import json
# jsonString = '{"bot_token": "bottoken", "bot_logging_channel": "botlogging", "bot_alias": "ss", "maximize_windows": true, "bot_name": "botname"}'
# x = ConfigurationModel.Parse(jsonString)
# print(str(x))
# print json.dumps(x.__dict__)