import JsonModel

class CommandModel(JsonModel.JsonModel):
    def __init__(self):
        self.command = None
        self.params = None
        self.description = None

    def ParseDict(self,obj):
        self.command = obj["command"]
        self.params = obj["params"] if "params" in obj  else []  
        self.description = obj["description"] if "description" in obj  else None


    @classmethod
    def Parse(cls,obj):
        cmdObj = cls()
        cmdObj.DoParse(obj)
        return cmdObj
    
    def __str__(self):
        return "\n\t\tCommand:\t\t{0}\n\t\tDescription:\t{1}\n\t\tParameters:\t\t{2}".format(self.command, self.description,self.params)

# jsonString = '{"command":"press", "params":["a","b","c"]}'
# x = CommandModel.Parse(jsonString)
# print(str(x))
# print json.dumps(x.__dict__)