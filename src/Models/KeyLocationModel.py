import JsonModel

class KeyLocationModel(JsonModel.JsonModel):
    def __init__(self):
        self.key = None
        self.loc_x = None
        self.loc_y = None

    def ParseDict(self,obj):
        self.key = obj["key"]
        self.loc_x = obj["loc_x"]
        self.loc_y = obj["loc_y"]

    @classmethod
    def Parse(cls,obj):
        cmdObj = cls()
        cmdObj.DoParse(obj)
        return cmdObj

# import json
# jsonString = '{"key":"a", "loc_x":1,"loc_y":3}'
# x = KeyLocationModel.Parse(jsonString)
# print(str(x))
# print json.dumps(x.__dict__)