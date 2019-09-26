import ScreenHelper

class Command(object):
    def __init__(self,container):
        self.screen_helper = ScreenHelper.ScreenHelper(container)
        self.os_service = container.GetProvider("OsService")
        self.commands = {
            "snap" : self.snap,
            "help" : self.help,
            "windows" : self.windows
        }

    def process(self, user, command):
        responseUser = "<@" + user + ">: "
        commandTrigger = command.split(' ')[0]
        commandParams = command.split(' ')[1:]
        if commandTrigger in self.commands:
            response = self.commands[commandTrigger](commandParams)
        else:
            response = ("text","Unknown command")
        
        return (response, responseUser)

    def snap(self, params):
        if(len(params) == 1):
            return ("file", self.screen_helper.save_screen_with_timestamp(params[0]))
        else:          
            return ("text","Expecting only 1 param")


    def help(self,params):
        response = "Available Commands:\r\n"

        for command in self.commands:
            response += command + "\r\b"

        return ("text",response)

    def windows(self,params):
        response = "I currently have the following windows open:\r\n"
        levels = 0 if (len(params) == 0) else int(params[0])
        self.os_service.PopulateWindowsEnumChild(levels)
        response +=  self.os_service.PrintTree()

        return ("content",response)