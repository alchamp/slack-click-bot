import Managers.Configuration as Configuration
import Managers.WindowManager as WindowManager
import Managers.EventManager as EventManager
import Managers.BotManager as BotManager
import Managers.WorkFlowCommandManager as WorkFlowCommandManager
import Managers.WorkflowExecutor as WorkflowExecutor
import Managers.LogManager as LogManager
import Managers.OnScreenKeyboardManager as OnScreenKeyboardManager


import Helpers.ScreenHelper as ScreenHelper

import Services.InteractionService as InteractionService
import Services.OsService as OsService
import Services.BotService as BotService
import Services.WorkFlowService as WorkFlowService
import Services.SlackCommandService as SlackCommandService

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
            "EventManager" : EventManager.EventManager(self),
            "SlackCommandService" : SlackCommandService.SlackCommandService(self),
            "WorkFlowService" : WorkFlowService.WorkFlowService(self),
            "WorkFlowCommandManager" : WorkFlowCommandManager.WorkFlowCommandManager(self),
            "WorkflowExecutor" : WorkflowExecutor.WorkflowExecutor(self),
            "LogManager" : LogManager.LogManager(self),
            "OnScreenKeyboardManager" : OnScreenKeyboardManager.OnScreenKeyboardManager(self)
        }
    
    def GetProvider(self,name):
        return self.providers[name]

    def Logger(self):
        return self.GetProvider("LogManager").GetLogger()