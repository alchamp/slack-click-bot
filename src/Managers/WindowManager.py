import win32gui
import time
import ctypes
import ctypes.wintypes
#import win32com.client

def get_actual_rect(osHandlerModel):
    try:
        f = ctypes.windll.dwmapi.DwmGetWindowAttribute
    except WindowsError:
        f = None
    if f:
        rect = ctypes.wintypes.RECT()
        DWMWA_EXTENDED_FRAME_BOUNDS = 9
        f(ctypes.wintypes.HWND(osHandlerModel.GetHandlePtr()),
        ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
        ctypes.byref(rect),
        ctypes.sizeof(rect)
        )
        bounds = (rect.left, rect.top, rect.right, rect.bottom)        
    else:      
        bounds = GetRect(osHandlerModel)
    return bounds 

def GetRect(osHandlerModel):
    (left, top, right, bottom) = win32gui.GetWindowRect(osHandlerModel.GetHandlePtr())
    return (left, top, right, bottom) 

class WindowManager(object):
    def __init__(self,container):
        self._container = container
        #self.shell = win32com.client.Dispatch("WScript.Shell")
        pass
    
    def GetInteractionService(self):
        return self._container.GetProvider("InteractionService")
        
    def BringForward(self, osHandlerModel):
        self.GetInteractionService().PressAlt()
        win32gui.SetForegroundWindow(osHandlerModel.GetHandlePtr())
    
    def Maximize(self, osHandlerModel):
        win32gui.ShowWindow(osHandlerModel.GetHandlePtr(), 3)
    
    def Restore(self,  osHandlerModel):
        win32gui.ShowWindow(osHandlerModel.GetHandlePtr(), 9)

    def GetScreenPositionTopLeft(self,  osHandlerModel):
        o = get_actual_rect(osHandlerModel)
        return (o[0],o[1])
    
    def GetWidthHeight(self,osHandlerModel):
        (left, top, right, bottom)  = get_actual_rect(osHandlerModel)
        print "t"+ str((left, top, right, bottom))
        height = bottom - top
        width = right - left
        return (width , height) 

    def GetWindowPointToScreen(self,  osHandlerModel, fromLeft,fromTop):
        (left, top, right, bottom)  = get_actual_rect(osHandlerModel)
        if(fromLeft >= 0 and fromTop >= 0 and right > fromLeft and bottom > fromTop):
            return (left + fromLeft, top + fromTop)
        return None

    def GetArea(self,osHandlerModel):
        (left, top, right, bottom)  = get_actual_rect(osHandlerModel)
        height = bottom - top
        width = right - left
        return height * width

    def GetLeftTopWidthHeight(self,osHandlerModel):
        (left,top) = self.GetScreenPositionTopLeft(osHandlerModel)
        (width,height) = self.GetWidthHeight(osHandlerModel)
        return (left,top,width,height)
    
        

