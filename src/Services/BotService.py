from slackclient import SlackClient
import time 

class BotService(object):
    def __init__(self,container):
        self._client = None
        self._name = None
        self._id = None
    
    def initialize(self,token,name):
        self._client = SlackClient(token)
        self._name = name     
        self._id = self._GetIdByName()
        if self._id is None:
            exit("Error could not find" + self._name)

    def IsReady(self):
        return self._id <> None and  self._client.rtm_connect(with_team_state= False)

    def GetId(self):
        return self._id 

    def _GetIdByName(self):
        api_call = self._client.api_call("users.list")
        if api_call.get('ok'):
            # find bot id by name
            users = api_call.get('members')
            for user in users:
                if 'name' in user and user.get('name') == self._name:
                    return "<@" + user.get('id') + ">"
            return None


    def ListenForEvents(self, sleepTime, processEventCallBack):
        if self._client.rtm_connect(with_team_state= False):
            print "Starting"
            while True:
                for event in self.ReadEvents():
                    processEventCallBack(event)
                time.sleep(sleepTime)
        else:
            exit("ERROR, Connection Failed")
    
    def ReadEvents(self):
        return self._client.rtm_read()

    def UploadFile(self, channel,filename, fileLocation):
        self._client.api_call('files.upload', channels=channel, filename=filename, file=open(fileLocation, 'rb'))

    def UploadSnippet(self,channel,content):
        self._client.api_call('files.upload', channels=channel, content=content)

    def PostTextMessage(self,userToAddress, channel, message):
        finalUserName = None
        if(userToAddress <> None and len(userToAddress) > 1 and userToAddress[:1] <> "@"):
            userToAddress = "@" + userToAddress
        finalUserName = userToAddress if userToAddress <> None else ""
        finalResponse = finalUserName + message
        self._client.api_call("chat.postMessage", channel=channel,text=finalResponse,as_user = True)