import Managers.Configuration as Configuration
import Managers.WindowManager as WindowManager
import Managers.EventManager as EventManager
import Managers.BotManager as BotManager

import Helpers.ScreenHelper as ScreenHelper

import Services.InteractionService as InteractionService
import Services.OsService as OsService
import Services.BotService as BotService

import Managers.Command as Command

#Bad
class Container(object):
    def __init__(self):
        self.providers = {
            "Configuration" : Configuration.Configuration(),
            "OsService" : OsService.OsService(self),
            "WindowManager": WindowManager.WindowManager(self),
            "ScreenHelper" : ScreenHelper.ScreenHelper(self),
            "InteractionService" : InteractionService.InteractionService(self),
            "BotService" : BotService.BotService(self),
            "BotManager" : BotManager.BotManager(self),
            "CommandManager" : Command.Command(self),
            "EventManager" : EventManager.EventManager(self)
        }
    
    def GetProvider(self,name):
        return self.providers[name]