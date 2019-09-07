import Configuration

class Container(object):
    def __init__(self):
        self.providers = {
            "Configuration" : Configuration.Configuration(),
        }
    
    def GetProvider(self,name):
        return self.providers[name]