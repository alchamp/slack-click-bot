import Managers.Configuration as Configuration
import Managers.OsService as OsService
import Managers.WindowService as WindowService
import Helpers.ScreenHelper as ScreenHelper
class Container(object):
    def __init__(self):
        self.providers = {
            "Configuration" : Configuration.Configuration(),
            "OsService" : OsService.OsService(self),
            "WindowService": WindowService.WindowService(self),
            "ScreenHelper" : ScreenHelper.ScreenHelper(self)
        }
    
    def GetProvider(self,name):
        return self.providers[name]