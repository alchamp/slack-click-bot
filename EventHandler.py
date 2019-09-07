import Command

class EventHandler:
    def __init__(self, bot,container):
        self.bot = bot
        self.command = Command.Command(container)

    def wait_for_event(self):
        events = self.bot.client.rtm_read()

        if events and len(events) > 0:
            for event in events:
                self.parse_event(event)
    
    def parse_event(self,event):
        if event and 'text' in event and self.bot.id in event['text']:
            self.process_event(event['user'], event['text'].split(self.bot.id)[1].strip().lower(), event['channel'])

    def process_event(self,user,command,channel):
        if command and channel:
            print "Command: " + command + " Channel: " + channel +" User: " + user
            response = self.command.process(user,command)
            print str(response)            
            if(response[0][0] == 'text'):
                finalResponse = response[1] + response[0][1]
                self.bot.client.api_call("chat.postMessage", channel=channel,text=finalResponse,as_user = True)
            elif(response[0][0]=='file'):
                self.bot.client.api_call('files.upload', channels=channel, filename='Test.png', file=open(response[0][1], 'rb'))
