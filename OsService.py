import win32gui
import win32con
import pyautogui
import time
import OsHandlerModel

def PopulateWindowHandler(hwnd,data):
    name = win32gui.GetWindowText(hwnd)
    isWindow =  win32gui.IsWindow(hwnd)
    if not not name and isWindow:
        osHandlerModel = OsHandlerModel.OsHandlerModel(data[1],hwnd,name)
        if data[1] > 0:
            try:
                if data[0]:
                    win32gui.EnumChildWindows(hwnd,PopulateWindowHandler,(data[0], data[1] - 1,osHandlerModel))
                else:
                    win32gui.EnumThreadWindows(hwnd,PopulateWindowHandler,(data[0], data[1] - 1,osHandlerModel))
            except:
                pass
        data[2].addChild(osHandlerModel)

def UserFriendlyTreePrintOut(osHandlerModel,tabs):
    currentNode =  str(len(tabs.split("\t"))) + " :: " + osHandlerModel.ToString() + "\n"

    if len(osHandlerModel.GetChildern()) == None:
        return "" 

    tabs += "\t"
    for child in osHandlerModel.GetChildern():
       currentNode += tabs + UserFriendlyTreePrintOut(child,str(tabs))
    
    return currentNode

class OsService(object):
    def __init__(self,container):
        self._rootOsHandlerModel = None
        pass

    def PopulateWindowsEnumChild(self,  level):
        del self._rootOsHandlerModel
        self._rootOsHandlerModel = OsHandlerModel.OsHandlerModel(0,-1,"root")
        win32gui.EnumWindows(PopulateWindowHandler,(True,level,self._rootOsHandlerModel))


    def PopulateWindowsEnumThread(self,  level):
        del self._rootOsHandlerModel
        self._rootOsHandlerModel = OsHandlerModel.OsHandlerModel(0,-1,"root")
        win32gui.EnumWindows(PopulateWindowHandler,(False,level,self._rootOsHandlerModel))

    def PrintTree(self):
        if self._rootOsHandlerModel <> None:
            return UserFriendlyTreePrintOut(self._rootOsHandlerModel,"")
        else:
            return "Root Os Handler Model Not Set" 



