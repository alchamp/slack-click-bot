import win32gui
import src.Models.OsHandlerModel as OsHandlerModel
import os
import time

def PopulateWindowHandler(hwnd,data):
    name = win32gui.GetWindowText(hwnd)
    isWindow =  win32gui.IsWindow(hwnd)
    if not not name and isWindow:
        osHandlerModel = OsHandlerModel.OsHandlerModel(data[1],hwnd,name,data[2])
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

def FindNodeInTree(osHandlerModel,nodeName,levels,currentLevel,excludedNames):
    if currentLevel > levels:
        return None
    
    winname = osHandlerModel.GetName().decode(encoding='UTF-8',errors='ignore').lower()
    nodeNameIn = nodeName.decode(encoding='UTF-8',errors='ignore').lower()
    if nodeNameIn in winname: 
        foundEx = False
        for exName in excludedNames:
             uuu = exName.decode(encoding='UTF-8',errors='ignore').lower()
             if uuu in winname: 
                 foundEx = True
        if foundEx == False:
            return osHandlerModel

    if len(osHandlerModel.GetChildern()) == None:
        return None 

    found = None
    for child in osHandlerModel.GetChildern():
        found = FindNodeInTree(child,nodeName,levels,currentLevel + 1,excludedNames)
        if found <> None: 
            break        

    return found

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
    
    def GetWindowByName(self, name, levels,excludedNames = []):
        if self._rootOsHandlerModel <> None:
            return FindNodeInTree(self._rootOsHandlerModel,name.lower(),levels,0,excludedNames)
        else:
            return None

    def StartProgram(self,programPath):
        try:
            os.startfile(programPath)
            return True
        except: 
            return False
        
    # used for bringing window forward
    def Sleep(self,seconds):
        time.sleep(seconds)