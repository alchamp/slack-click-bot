import JsonModel
import CommandModel

class WorkFlowModel(JsonModel.JsonModel):
    def __init__(self,name):
        self.name = name
        self.windowname = None
        self.commands = []
        self.argcount = None

    def ParseDict(self,obj):
        self.windowname = obj["windowname"]
        self.argcount = obj["argcount"] if "argcount" in obj  else None
        commands = obj["commands"] if "commands" in obj  else []

        for cmd in commands:
            self.commands.append(CommandModel.CommandModel.Parse(cmd))

    @classmethod
    def Parse(cls,obj,name):
        cmdObj = cls(name)
        cmdObj.DoParse(obj)
        return cmdObj

# jsonString = '''
# {
#    "argcount": 3,
#     "windowname":"NotePad++",
#     "commands":[ 
#         {"command":"press", "params":["a","b","c"]},
#         {"command":"type", "params":["d","a","f"]} 
#         ]
# }
# '''
# x = WorkFlowModel.Parse(jsonString,"wf1")
# print "Hello"
# print json.dumps(x.__dict__)