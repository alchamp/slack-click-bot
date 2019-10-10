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
        self._container.Logger().info("Logging In")
        token = self.GetConfigManager().GetBotToken()
        name = self.GetConfigManager().GetBotName()      
        logging = self.GetConfigManager().GetBotLoggingChannelName()    
        self.GetBotService().initialize(token,name,logging)
        self._container.Logger().info("Logged In")

    def IsReady(self):
        return self.GetBotService().IsReady()

    def Start(self):
        if self.IsReady():
            callback = self.GetProcessEventCallBack()
            self._container.Logger().info("Starting")
            self._container.Logger().info("Waiting for commands")
            while True:
                try:
                    events = self.GetBotService().ReadEvents()
                    if events and len(events) > 0:
                        for event in events:
                            callback(event)
                    time.sleep(1)
                except Exception as error:
                    user = "<@" + event['user'] + ">: "
                    self._container.Logger().exception(error)
                    self.GetBotService().PostTextMessage(user,event['channel'], "!!COMMAND FAILED!! Check #"+ str(self.GetConfigManager().GetBotLoggingChannelName())  +" for more info")
                    if not self.GetConfigManager().GetAlwaysOn():
                        raise                        
        else:
            exit("ERROR, Connection Failed")       
