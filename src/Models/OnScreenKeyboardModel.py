class OnScreenKeyboardModel(object):
    def __init__(self,key,centerXY):
        self._key = key
        self._centerXY = centerXY

    def GetKey(self):
        return self._key

    def GetCenter(self):
        return self._centerXY
    
    def ToString(self):
        return str(self._key) + " " + str((self._centerXY.x,self._centerXY.y))