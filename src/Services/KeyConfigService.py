import os
import src.Models.KeyboardConfigModel as KeyboardConfigModel

class KeyConfigService(object):
    def __init__(self,container):
        self._container = container
        self._keyboardConfigModel = None
        self._loaded = False

    def LoadKeyConfig(self,path):
        with open(path) as f:
            self._keyboardConfigModel  = KeyboardConfigModel.KeyboardConfigModel.Parse(f.read())
        self._loaded = True
   
    def GetKeyboardConfigModel(self):
        return self._keyboardConfigModel
    
    def GetWidthHeight(self):
        width = 0
        height = 0
        if self._loaded:
            width = self._keyboardConfigModel.width
            height = self._keyboardConfigModel.height
        return (width,height) 
    
    def GetAllKeyLocationModels(self):
        if self._loaded:
            return self._keyboardConfigModel.all_keys
        else:
            return None
