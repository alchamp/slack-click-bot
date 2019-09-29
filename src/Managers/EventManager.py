import time
import Command
class EventManager(object):
    def __init__(self,container):
        self._container = container

    def GetCommandManager(self):
        return self._container.GetProvider("CommandManager")

    def GetBotService(self):
        return self._container.GetProvider("BotService")
    
    def GetAlias(self):
        return self._container.GetProvider("Configuration").GetTriggerAlias()

    def GetProcessEventCallBack(self):
        return self.CallBack

    def CallBack(self,event):
        (command,user,channel) = self.ParseEvent(event)
        if command <> None:
            self.ProcessEvent(user,command,channel)  
    
    def ProcessEvent(self,user,command,channel):
        if command and channel:
            print "Command: " + command + " Channel: " + channel +" User: " + user
            response = self.GetCommandManager().ProcessCommand(user,channel,command)
            print str(response)            
            if(response[0][0] == 'text'):
                self.GetBotService().PostTextMessage(response[1],channel, response[0][1])
            elif(response[0][0]=='file'):
                self.GetBotService().UploadFile(channel, '',response[0][1])
            elif(response[0][0]=='content'):
                self.GetBotService().UploadSnippet(channel, response[0][1])
     
    def ParseEvent(self,event):
        command = self.GetCommand(event)
        if command == None:
            return (None,None,None)
        return (command, event['user'] , event['channel']) 

    #None,1 = TriggerByName,2 = TriggerByAlias
    def GetEventType(self, event):
         triggerName = event and 'text' in event and self.GetBotService().GetId() in event['text']
         triggerSS = (not triggerName
         and event
         and 'text' in event 
         and event.get('type') == 'message'
         and len(event['text']) > len(self.GetAlias()) + 1
         and self.GetAlias() == event['text'][:len(self.GetAlias())])  

         if(triggerName):
            return 1
         elif(triggerSS):
            return 2
         else:
             return None
    
    def GetCommand(self,event):
        eventType = self.GetEventType(event)
        if(eventType == 1):
            return event['text'].split(self.GetBotService().GetId())[1].strip().lower()
        elif(eventType == 2):
            return event['text'].split(self.GetAlias())[1].strip().lower()
        return None