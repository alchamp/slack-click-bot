import JsonModel
import KeyLocationModel

class KeyboardConfigModel(JsonModel.JsonModel):
    def __init__(self):
        self.height = None
        self.width = None
        self.all_keys = []

    def ParseDict(self,obj):
        self.height = int(obj["height"])
        self.width = int(obj["width"])
        keys = obj["all_keys"] if "all_keys" in obj  else []
        for key in keys:
            keyLocationModel =  KeyLocationModel.KeyLocationModel.Parse(key)
            self.all_keys.append(keyLocationModel)

    @classmethod
    def Parse(cls,obj):
        cmdObj = cls()
        cmdObj.DoParse(obj)
        return cmdObj

# import json
# #jsonString = '{"height":200,"width":100}'
# jsonString = '{"height":200,"width":100,"all_keys":[{"key":"a", "loc_x":1,"loc_y":3},{"key":"b", "loc_x":3,"loc_y":5}]}'
# x = KeyboardConfigModel.Parse(jsonString)
# print(str(x))
