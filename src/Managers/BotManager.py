import time

class BotManager(object):
    def __init__(self,container):
        self._container = container
        
    def GetBotService(self):
        return self._container.GetProvider("BotService")

    def GetConfigManager(self):
        return self._container.GetProvider("Configuration")

    def GetProcessEventCallBack(self):
        return self._container.GetProvider("EventManager").GetProcessEventCallBack()

    def Login(self):
        print "Logging In"
        token = self.GetConfigManager().GetBotToken()
        name = self.GetConfigManager().GetBotName()      
        self.GetBotService().initialize(token,name)

    def IsReady(self):
        return self.GetBotService().IsReady()

    def Start(self):
        if self.IsReady():
            callback = self.GetProcessEventCallBack()
            print "Starting"
            while True:
                events = self.GetBotService().ReadEvents()
                if events and len(events) > 0:
                    for event in events:
                        callback(event)
                time.sleep(1)
        else:
            exit("ERROR, Connection Failed")       
