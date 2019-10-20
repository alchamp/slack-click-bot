import json
from abc import ABCMeta, abstractmethod

class JsonModel():
    __metaclass__ = ABCMeta
    
    def DoParse(self,x):
        if(isinstance(x,str)):
            self.ParseJson(x)
        else:
            self.ParseDict(x)

    def ParseJson(self,jsonString):
        self.ParseDict(json.loads(jsonString))

    def ParseBool(self, obj, fieldKey):
        value = False
        valueIn = obj[fieldKey] if fieldKey in obj  else False
        if(isinstance(valueIn, basestring)):
            valueIn.decode(encoding='UTF-8',errors='ignore').lower()
            if(valueIn == "true" or valueIn == "y" or valueIn == "yes"):
                value = True
        else:
             value = (valueIn == True)
        return value

    @abstractmethod
    def ParseDict(self,obj):
        pass
        