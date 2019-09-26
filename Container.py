import Configuration
import OsService

class Container(object):
    def __init__(self):
        self.providers = {
            "Configuration" : Configuration.Configuration(),
            "OsService" : OsService.OsService(self),
        }
    
    def GetProvider(self,name):
        return self.providers[name]