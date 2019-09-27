import src.Helpers.ScreenHelper as ScreenHelper

class Command(object):
    def __init__(self,container):
        self._container = container
        self.screen_helper = ScreenHelper.ScreenHelper(container)
        self.os_service = container.GetProvider("OsService")
        self.commands = {
            "snap" : self.snap,
            "help" : self.help,
            "windows" : self.windows,
            "raw" : self.raw
        }

    def _GetWindowService(self):
        return self._container.GetProvider("WindowService")

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

    def raw(self, params):
        if(len(params) > 0):
            name = " ".join(params)
            self.os_service.PopulateWindowsEnumChild(1)
            model = self.os_service.GetWindowByName(name, 1)
            if model:
                self._GetWindowService().BringForward(model)
                return ("file", self.screen_helper.realSaveScreen("raw", self._GetWindowService().GetLeftTopWidthHeight(model)))
            else:
                return ("text","Could Not Find Window: " + name)
        else:          
            return ("text","Expecting String after `name`")

