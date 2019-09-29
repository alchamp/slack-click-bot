import JsonModel
import WorkFlowModel

class SlackCommandModel(JsonModel.JsonModel):
    def __init__(self, name):
        self.workflows = []
        self.name = name
        
    def GetWorkflows(self):
        return self.workflows
        
    def GetName(self):
        return self.name

    def ParseDict(self,obj):
        self.workflows = obj["workflows"]
       
    @classmethod
    def Parse(cls,obj,name):
        cmdObj = cls(name)
        cmdObj.DoParse(obj)
        return cmdObj

# jsonString = '''
# {
 
#     "workflows":[ 
#         "doSomething",
#         "doSomething2"
#         ]
# }
# '''
# x = SlackCommandModel.Parse(jsonString,"rv")
# print "Hello"
# print json.dumps(x.__dict__)