import os
import src.Models.SlackCommandModel as SlackCommandModel

class SlackCommandService(object):
    def __init__(self,container):
        self._container = container
        self.directory = os.path.join(os.getcwd(), "commands\slackcommands")
        self.slackCommands = {}

    def LoadSlackCommands(self):
        for filename in os.listdir( self.directory ):
            if filename.endswith(".json"): 
                nameWithoutExtension = filename.split(".")[0]
                with open(os.path.join(self.directory, filename)) as f:
                    self.slackCommands[nameWithoutExtension] = SlackCommandModel.SlackCommandModel.Parse(f.read(),nameWithoutExtension)
            else:
                continue

    def GetAllCommandsNames(self):
        return self.slackCommands.keys()

    def GetAllCommands(self):
        return self.slackCommands.values()

    def GetSlackCommandByName(self, name):
        return self.slackCommands[name]

    def SlackCommandExistByName(self, name):
        return name in self.slackCommands    
