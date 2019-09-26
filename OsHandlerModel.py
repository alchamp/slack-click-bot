class OsHandlerModel(object):
    def __init__(self,level,hwndPtr,name):
        self._hwnd = hwndPtr
        self._name = name
        self._childern = []
        self._level = level
    
    def addChild(self, child):
        if isinstance(child, OsHandlerModel):
            self._childern.append(child)
        else:
            raise Exception("child is not an instance of OSHandler")

    def GetLevel(self):
        return self._level
    def GetName(self):
        return self._name    

    def GetHandlePtr(self):
        return self._hwnd
    def GetChildern(self):
        return self._childern

    def IsRoot(self):
        return self._hwnd == -1
    
    def ToString(self):
        return str(self.GetHandlePtr()) + " - "+ self.GetName()