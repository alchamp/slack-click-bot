import time 
import EventHandler
from slackclient import SlackClient

class Bot(object):
    def __init__(self,container):
        config = container.GetProvider("Configuration")
        self.client = SlackClient(config.bot_token)
        self.name = config.bot_name
        self.id = self.get_id_by_name()

        if self.id is None:
            exit("Error could not find" + self.name)
        
        self.event = EventHandler.EventHandler(self,container)
      
    def get_id_by_name(self):
        api_call = self.client.api_call("users.list")
        if api_call.get('ok'):
            # find bot id by name
            users = api_call.get('members')
            for user in users:
                if 'name' in user and user.get('name') == self.name:
                    return "<@" + user.get('id') + ">"
            return None

    def start_listening_for_events(self):
        if self.client.rtm_connect(with_team_state= False):
            print "Starting"
            while True:
                self.event.wait_for_event()
                time.sleep(1)
        else:
            exit("ERROR, Connection Failed")