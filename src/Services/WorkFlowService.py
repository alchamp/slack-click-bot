import os
import src.Models.WorkFlowModel as WorkFlowModel

class WorkFlowService(object):
    def __init__(self,container):
        self._container = container
        self.workflowDir = os.path.join(os.getcwd(), "commands\\workflows")
        self.workflows = {}

    def LoadWorkflows(self):
        for filename in os.listdir( self.workflowDir ):
            if filename.endswith(".json"): 
                workflowName = filename.split(".")[0]
                with open(os.path.join(self.workflowDir, filename)) as f:
                    self.workflows[workflowName] = WorkFlowModel.WorkFlowModel.Parse(f.read(),workflowName)
            else:
                continue

    def GetWorkflowByName(self, name):
        return self.workflows[name]

    
    def WorkflowExistByName(self, name):
        return name in self.workflows    
