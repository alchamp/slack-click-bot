class Command(object):
    def __init__(self,container):
        self._container = container
        self.commands = {
            "help" : self.help,
            "windows" : self.windows,
            "raw" : self.raw,
            "testerror": self.testerror
        }

    def _GetScreenHelper(self):
        return self._container.GetProvider("ScreenHelper")

    def _GetOsService(self):
        return self._container.GetProvider("OsService")

    def _GetWindowManager(self):
        return self._container.GetProvider("WindowManager")
    
    def GetWorkFlowCommandManager(self):
        return self._container.GetProvider("WorkFlowCommandManager")
    
    def GetWorkflowExecutor(self):
        return self._container.GetProvider("WorkflowExecutor")

    def ProcessCommand(self, user,channel, command):
         return  self.process( user,channel, command)

    def process(self, user, channel,command):
        responseUser = user
        commandTrigger = command.split(' ')[0]
        commandParams = command.split(' ')[1:]
        if commandTrigger in self.commands:
            response = self.commands[commandTrigger](commandParams)
        elif self.GetWorkFlowCommandManager().HasCommand(commandTrigger):
            self.GetWorkflowExecutor().Execute(commandTrigger,commandParams,channel,user)
            response = ("text","Done Proccessing Workflow command")
        else:
            response = ("text","Unknown command")
        
        return (response, responseUser)


    def help(self,params):
        response = "\r\nAvailable Commands:\r\n"

        for command in self.commands:
            response += command + "\r\b"
        
        response += "\r\nAvailable Workflow Commands:\r\n"
        for workflowCommand in self.GetWorkFlowCommandManager().GetCommandNames():
            response += workflowCommand + "\r\b"

        return ("text",response)

    def windows(self,params):
        response = "I currently have the following windows open:\r\n"
        levels = 0 if (len(params) == 0) else int(params[0])
        self._GetOsService().PopulateWindowsEnumChild(levels)
        response +=  self._GetOsService().PrintTree()

        return ("content",response)

    def raw(self, params):
        if(len(params) > 0):
            name = " ".join(params)
            self._GetOsService().PopulateWindowsEnumChild(1)
            model = self._GetOsService().GetWindowByName(name, 1)
            if model:
                self._GetWindowManager().BringForward(model)
                return ("file", self._GetScreenHelper().realSaveScreen("raw", self._GetWindowManager().GetLeftTopWidthHeight(model)))
            else:
                return ("text","Could Not Find Window: " + name)
        else:          
            return ("text","Expecting String after `name`")
       
    def testerror(self,params):
        raise Exception("This is an exception test")
