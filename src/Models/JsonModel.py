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



    @abstractmethod
    def ParseDict(self,obj):
        pass
        