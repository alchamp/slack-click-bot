import JsonModel

class CommandModel(JsonModel.JsonModel):
    def __init__(self):
        self.command = None
        self.params = None

    def ParseDict(self,obj):
        self.command = obj["command"]
        self.params = obj["params"] if "params" in obj  else []  

    @classmethod
    def Parse(cls,obj):
        cmdObj = cls()
        cmdObj.DoParse(obj)
        return cmdObj

# jsonString = '{"command":"press", "params":["a","b","c"]}'
# x = CommandModel.Parse(jsonString)
# print(str(x))
# print json.dumps(x.__dict__)