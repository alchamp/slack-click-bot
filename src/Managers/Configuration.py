import os
import src.Models.ConfigurationModel as ConfigurationModel

class Configuration(object):
    def __init__(self):
        self.config_file_path = os.path.join(os.getcwd(), "bot.config")
        configurationModel = None
        #Read config file
        with open(self.config_file_path) as f:
            configurationModel = ConfigurationModel.ConfigurationModel.Parse(f.read())
        
        self.bot_token = configurationModel.GetToken()
        self.bot_name = configurationModel.GetName()
        self.bot_alias = configurationModel.GetAlias()
        self.bot_logging_channel = configurationModel.GetLoggingChannel()
        self.bot_should_max_windows = configurationModel.ShouldMaximizeWindows()
        self.bot_keys_folder = configurationModel.GetKeysFolderPath()
        if self.bot_keys_folder == None:
            self.bot_keys_folder = os.path.join(os.getcwd(), "src\\Services\\keys")


    def GetBotToken(self):
        return self.bot_token 

    def GetBotName(self):
        return self.bot_name 
    
    def GetTriggerAlias(self):
        return self.bot_alias
    
    def GetAlwaysOn(self):
        return True

    def GetBotLoggingChannelName(self):
        return self.bot_logging_channel

    def ShouldMaximizeWindows(self):
        return self.bot_should_max_windows
        
    def GetOnScreenKeyboardKeys(self):
        return self.bot_keys_folder