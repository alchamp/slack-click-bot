import os
import src.Models.OnScreenKeyboardModel as OnScreenKeyboardModel
import time
class OnScreenKeyboardManager(object):
    def __init__(self,container):
        self._container = container
        self._availableKeys = {}
        self._windowName = "on-screen keyboard"
        self._currentHandle = None
        self._isEnabled = True

    def IsEnabled(self):
        return self._isEnabled

    def Initialize(self):
        self.LoadKeys()
        
    def GetConfiguration(self):
        return self._container.GetProvider("Configuration")
    def GetWindowManager(self):
        return self._container.GetProvider("WindowManager")
    def GetOsService(self):
        return self._container.GetProvider("OsService")     
    def GetInteractionService(self):
        return self._container.GetProvider("InteractionService")
             
    def _ShowHide(self,show):
        self.GetOsService().PopulateWindowsEnumChild(1)
        ps = self.GetOsService().GetWindowByName(self._windowName ,1)
        if((show and ps == None) or (not show and ps <> None) ):
            self.GetInteractionService().ProcessHotkey(('ctrlleft','winleft','o'))
            time.sleep(.5)
            self.GetOsService().PopulateWindowsEnumChild(1)
            ps = self.GetOsService().GetWindowByName(self._windowName ,1)
        self._currentHandle = ps

    def Show(self):
        self._container.Logger().info("Show On Screen Keyboard ")
        self._ShowHide(True)
        
    def Hide(self):
        self._container.Logger().info("Hide On Screen Keyboard ")
        self._ShowHide(False)

    def KeyAvailable(self,key):
        return key in self._availableKeys

    def HasAllKeyAvailable(self,keys):
        for key in keys:
            if self.KeyAvailable(key) == False:
                return False
        return True
          
    def ClickAvailableKeys(self,keys):
        self.Show()
        for key in keys:            
            self._ClickAvailableKey(key)
            time.sleep(.1)
        self.Hide()

    def _ClickAvailableKey(self,key):
        if self.KeyAvailable(key):
            k = self._availableKeys[key]
            c = k.GetCenter()
            self.GetInteractionService().ProcessClick((c.x,c.y))
    
    def AddKey(self,onScreenKeyboardModel):
        self._availableKeys[onScreenKeyboardModel.GetKey()] = onScreenKeyboardModel
   
    def ClearAllKeys(self):
        self._availableKeys = {}

    def GetAllKeys(self):
        return self._availableKeys.keys() 

    def LoadKeys(self):
        self.Show()
        self._container.Logger().info("Loading Keys For On Screen Keyboard ")
        keysFolder = self.GetConfiguration().GetOnScreenKeyboardKeys()
        for filename in os.listdir( keysFolder ):
            if filename.endswith(".png"): 
                keyKey = filename.split(".")[0]
                filePath = os.path.join(keysFolder, filename)
                self._container.Logger().info("Attempting to load " + str(filePath))
                center = self.GetWindowManager().LocateOnWindow(self._currentHandle,filePath)
                model = OnScreenKeyboardModel.OnScreenKeyboardModel(keyKey,center)
                self.AddKey(model)
                self._container.Logger().info("Found Key " + model.ToString())
            else:
                continue
        self.Hide()