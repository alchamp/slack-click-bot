import pyautogui
from datetime import datetime

#remove after testing
#pyautogui.PAUSE = 1.5
#remove after testing

class InteractionService(object):
    def __init__(self,container):
        self._container = container

    #x,y
    def ProcessClick(self,params):
        print "clicking " + str(params)
        pyautogui.click(int(params[0]),int(params[1]))

    #text
    def ProcessType(self,params):
        print "typing " + str(params)
        pyautogui.typewrite(params[0])

    #text[]
    def ProcessPress(self,params):
        print "pressing  " + str(params)
        pyautogui.typewrite(params)
        #text[]

    #hotkey[]
    def ProcessHotkey(self,params):
        print "hotkey  " + str(params)
        if len(params) == 2:
            pyautogui.hotkey(params[0],params[1]) 
        elif len(params) == 3:
            pyautogui.hotkey(params[0],params[1],params[2]) 

    # used for bringing window forward
    def PressAlt(self):
        pyautogui.press("alt")
