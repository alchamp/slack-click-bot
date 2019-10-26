import JsonModel

class ConfigurationModel(JsonModel.JsonModel):
    def __init__(self):
        self.bot_name = None
        self.bot_token = None
        self.bot_alias = None
        self.bot_logging_channel = None
        self.maximize_windows = False
        self.keys_folder_path = None
        self.keys_config = None
        self.keys_mode = None
        self.interpolate_clicks = None
        self.use_mss = None
        self.use_image_thread = None
        
    def ParseDict(self,obj):
        self.bot_name = obj["bot_name"]
        self.bot_token = obj["bot_token"]
        self.bot_alias = obj["bot_alias"] if "bot_alias" in obj  else "ss"
        self.bot_logging_channel = obj["bot_logging_channel"] if "bot_logging_channel" in obj  else None
        self.keys_folder_path = obj["keys_folder_path"] if "keys_folder_path" in obj  else None
        self.keys_config = obj["keys_config"] if "keys_config" in obj  else None
        self.keys_mode = obj["keys_mode"] if "keys_mode" in obj  else None
        self.maximize_windows = self.ParseBool(obj,"maximize_windows")
        self.interpolate_clicks = self.ParseBool(obj,"interpolate_clicks")
        self.use_mss = self.ParseBool(obj,"use_mss")
        self.use_image_thread = self.ParseBool(obj,"use_image_thread")

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
    
    def GetKeysFolderPath(self):
        return self.keys_folder_path
    
    def GetKeysConfig(self):
        return self.keys_config

    def GetKeysMode(self):
        return self.keys_mode

    def GetInterpolateClicks(self):
        return self.interpolate_clicks

    def GetUseMSS(self):
        return self.use_mss

    def GetUseImageThread(self):
        return self.use_image_thread
# import json
# jsonString = '{"bot_token": "bottoken", "bot_logging_channel": "botlogging", "bot_alias": "ss", "maximize_windows": true, "bot_name": "botname"}'
# x = ConfigurationModel.Parse(jsonString)
# print(str(x))
# print json.dumps(x.__dict__)