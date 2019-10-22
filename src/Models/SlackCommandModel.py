import JsonModel
import WorkFlowModel

class SlackCommandModel(JsonModel.JsonModel):
    def __init__(self, name):
        self.workflows = []
        self.name = name
        self.description = None

    def GetWorkflows(self):
        return self.workflows
        
    def GetName(self):
        return self.name

    def ParseDict(self,obj):
        self.workflows = obj["workflows"]
        self.description = obj["description"] if "description" in obj  else None 

    @classmethod
    def Parse(cls,obj,name):
        cmdObj = cls(name)
        cmdObj.DoParse(obj)
        return cmdObj

    def __str__(self):
        wfstr = []
        for wf in self.workflows:
            wfstr.append(str(wf))
        wfsString = "\n\t".join(wfstr)
        return "Command Name:\t{0},\nDescription:\t{1}\nWorkflows:\n\t{2}".format(self.name, self.description,wfsString)

# jsonString = '''
# {
 
#     "workflows":[ 
#         "doSomething",
#         "doSomething2"
#         ]
# }
# '''
# x = SlackCommandModel.Parse(jsonString,"rv")
#print x