
class WorkFlowCommandManager(object):
    def __init__(self,container):
        self._container = container
        self._ready = False

    def GetReady(self):
        return self._ready

    def GetSlackCommandService(self):
        return self._container.GetProvider("SlackCommandService")

    def GetWorkflowService(self):
        return self._container.GetProvider("WorkFlowService")

    def HasCommand(self,name):
        return self.GetSlackCommandService().SlackCommandExistByName(name)
    
    def GetCommand(self,name):
        return self.GetSlackCommandService().GetSlackCommandByName(name)

    def GetCommandNames(self):
        return self.GetSlackCommandService().GetAllCommandsNames()
    
    def GetCommandWorkFlows(self,name):
        cmd = self.GetSlackCommandService().GetSlackCommandByName(name)
        workflows = []
        for workflowName in cmd.GetWorkflows():
            workflows.append(self.GetWorkflowService().GetWorkflowByName(workflowName))
        return workflows

    def Initialize(self):
        self.GetWorkflowService().LoadWorkflows()
        self.GetSlackCommandService().LoadSlackCommands()

        for slackcmds in self.GetSlackCommandService().GetAllCommands():
            for workflowName in slackcmds.GetWorkflows():
                if  not self.GetWorkflowService().WorkflowExistByName(workflowName):
                    raise Exception("Missing Workflow " + workflowName + " in slack command: " + slackcmds.GetName())
        self._read = True