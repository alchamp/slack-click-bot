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
        self.bot_keys_config = configurationModel.GetKeysConfig()
        self.bot_keys_mode = configurationModel.GetKeysMode()
        self.bot_should_interpolate_clicks = configurationModel.GetInterpolateClicks()
        self.bot_uses_mss  = configurationModel.GetUseMSS()
        self.bot_uses_image_thread  = configurationModel.GetUseImageThread()  
        if self.bot_keys_folder == None:
            self.bot_keys_folder = os.path.join(os.getcwd(), "src\\Services\\keys")
        if self.bot_keys_config == None:
            self.bot_keys_config = os.path.join(os.getcwd(), "src\\Services\\keys\\keyboard.config")

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
        
    def GetOnScreenKeyboardKeys(self):
        return self.bot_keys_folder

    def GetOnScreenKeyboardConfig(self):
        return self.bot_keys_config       

    def GetOnScreenKeyboardMode(self):
        return self.bot_keys_mode

    def ShouldMaximizeWindows(self):
        return self.bot_should_max_windows

    def ShouldInterpolateClicks(self):
        return self.bot_should_interpolate_clicks
        
    def UseMSS(self):
        return self.bot_uses_mss

    def UseImageThread(self):
        return self.bot_uses_image_thread