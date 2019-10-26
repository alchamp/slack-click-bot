import os
import src.Models.OnScreenKeyboardModel as OnScreenKeyboardModel
import time
import pyautogui
class OnScreenKeyboardManager(object):
    def __init__(self,container):
        self._container = container
        self._availableKeys = {}
        self._windowName = "on-screen keyboard"
        self._program_path = "C:\\Windows\\System32\\osk.exe"
        self._currentHandle = None
        self._widthFactor = 1
        self._heightFactor = 1

    def IsEnabled(self):
        return self.GetConfiguration().GetOnScreenKeyboardMode() <> None and (self.IsConfigMode() or self.IsPNGMode())
    
    def IsConfigMode(self):
        mode = self.GetConfiguration().GetOnScreenKeyboardMode()
        return mode == "config"
    
    def IsPNGMode(self):
        mode = self.GetConfiguration().GetOnScreenKeyboardMode()
        return mode == "png"

    def Initialize(self):
        if self.IsEnabled():
            if self.IsPNGMode():
                self._container.Logger().info(" OnScreenKeyboardManager IsPNGMode")
                self.LoadKeysPNG()
            elif self.IsConfigMode():
                self.LoadKeysConfig()
                self._container.Logger().info(" OnScreenKeyboardManager IsConfigMode")        

    def GetConfiguration(self):
        return self._container.GetProvider("Configuration")
    def GetWindowManager(self):
        return self._container.GetProvider("WindowManager")
    def GetOsService(self):
        return self._container.GetProvider("OsService")     
    def GetInteractionService(self):
        return self._container.GetProvider("InteractionService")
    def GetKeyConfigService(self):
        return self._container.GetProvider("KeyConfigService")
    
    def _SetWidthHeightFactor(self):
        if self.IsPNGMode():
            self._widthFactor = 1
            self._heightFactor = 1   
        elif self.IsConfigMode(): 
            (origW,origH) = self.GetKeyConfigService().GetWidthHeight()      
            (wf, hf) = self.GetWindowManager().GetInterpolatedRatio(self._currentHandle,origW,origH)
            self._widthFactor = wf
            self._heightFactor = hf
            self._container.Logger().info(" WidthFactor: " + str(self._widthFactor) + " heightFactor: " + str(self._heightFactor))

    def _GetPoint(self, center):
        if self.IsPNGMode():
            return (center.x,center.y)
        elif self.IsConfigMode():
            (x,y) = self.GetWindowManager().GetWindowPointToScreenInterpolatedWithFactors(self._currentHandle,center.x,center.y,self._widthFactor,self._heightFactor)
            return(x,y)
    
    def _ShowHide(self,show):
        self.GetOsService().PopulateWindowsEnumChild(1)
        ps = self.GetOsService().GetWindowByName(self._windowName ,1)
        # if((show and ps == None)  ):
        #     self.GetInteractionService().ProcessHotkey(('ctrlleft','winleft','o')) #they are the same
        # elif((not show and ps <> None) ):
        #     self.GetInteractionService().ProcessHotkey(('ctrlleft','winleft','o'))

        if((show and ps == None)  ):
            self._LaunchProgram()
        elif((not show and ps <> None) ):
            self._KillProgram()

        if((show and ps == None) or (not show and ps <> None) ):
            time.sleep(.4)
            self.GetOsService().PopulateWindowsEnumChild(1)
            ps = self.GetOsService().GetWindowByName(self._windowName ,1)
        self._currentHandle = ps

    def _LaunchProgram(self):
        self.GetOsService().StartProgram(self._program_path)

    def _KillProgram(self):
         os.system("tskill osk")

    def Show(self):
        self._container.Logger().info("Show On Screen Keyboard ")
        self._ShowHide(True)
        self._SetWidthHeightFactor()
        
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
        self.ClickAvailableKeysWithDelay(keys,0.1)     

    def ClickAvailableKeysWithDelay(self,keys,delayFloat):
        self.Show()
        for key in keys:  
            time.sleep(delayFloat)          
            self._ClickAvailableKey(key)             
        self.Hide()

    def _ClickAvailableKey(self,key):
        if self.KeyAvailable(key):
            k = self._availableKeys[key]
            c = k.GetCenter()
            self.GetInteractionService().ProcessClick(self._GetPoint(c))
    
    def AddKey(self,onScreenKeyboardModel):
        self._availableKeys[onScreenKeyboardModel.GetKey()] = onScreenKeyboardModel
   
    def ClearAllKeys(self):
        self._availableKeys = {}

    def GetAllKeys(self):
        return self._availableKeys.keys() 

    def LoadKeysPNG(self):
        self.Show()
        self._container.Logger().info("Loading Keys For On Screen Keyboard Using PNG ")
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

    def LoadKeysConfig(self):
        self._container.Logger().info("Loading Keys For On Screen Keyboard Using Config")
        keysConfig = self.GetConfiguration().GetOnScreenKeyboardConfig()
        self.GetKeyConfigService().LoadKeyConfig(keysConfig)
        allKeyLocationModels = self.GetKeyConfigService().GetAllKeyLocationModels()
        if allKeyLocationModels <> None:
            for kl in allKeyLocationModels:
                model = OnScreenKeyboardModel.OnScreenKeyboardModel(kl.key,type('',(object,),{"x": kl.loc_x,"y": kl.loc_y})())
                self.AddKey(model)

