import JsonModel
import CommandModel

class WorkFlowModel(JsonModel.JsonModel):
    def __init__(self,name):
        self.name = name
        self.windowname = None
        self.excludednames = []
        self.commands = []
        self.argcount = None
        self.program = None
        self.programdelay = None
        self.originalheight = None
        self.originalwidth = None
        self.interpolateclicks = None

    def ParseDict(self,obj):
        self.windowname = obj["windowname"]
        self.argcount = obj["argcount"] if "argcount" in obj  else None
        self.originalheight = obj["originalheight"] if "originalheight" in obj  else None
        self.originalwidth = obj["originalwidth"] if "originalwidth" in obj  else None
        
        self.excludednames = obj["excludednames"] if "excludednames" in obj  else []
        self.program = obj["program"] if "program" in obj and obj["program"] != "" else None
        self.programdelay = int(obj["programdelay"]) if "programdelay" in obj and obj["programdelay"] != ""  else None

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