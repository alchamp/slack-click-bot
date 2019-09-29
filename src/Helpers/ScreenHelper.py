import pyautogui
import os 
from datetime import datetime
import time

#remove after testing
#pyautogui.PAUSE = 1.5
#remove after testing

class ScreenHelper(object):
    def __init__(self,container):
        self._container = container
        self.root_dir = self.create_year_directory()
        self.instructions = {
            "click" : self.process_click,
            "type" : self.process_type,
            "press" : self.process_press,
            "hotkey" : self.process_hotkey,
            "screenshot":self.process_screenshot
        }
    
    def _GetInteractionService(self):
        return self._container.GetProvider("InteractionService")

    def _GetWorkflow(self):
        return self._container.GetProvider("Configuration").instructions

    def create_year_directory(self):
        year = datetime.today().strftime('%Y')
        year_dir = os.path.join(os.getcwd(), year)
        try:
            if not os.path.isdir(year_dir):
                os.makedirs(year_dir)
        except OSError:
            print "Directory Exist"
        return year_dir

    def load_test_instructions(self):
        return ['click,1000,500','type,d_input','press,enter,a']

    def save_screen_with_timestamp(self,prefix,regionIn = None):
        self.do_instructions(prefix)

        timeStamp = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
        if regionIn <> None:
            pic = pyautogui.screenshot(region=regionIn)
        else:
            pic = pyautogui.screenshot()

        path = os.path.join(self.root_dir, prefix + '-' + timeStamp + '.png')
        pic.save(path)
        return path

    def realSaveScreen(self,prefix,regionIn = None):
        timeStamp = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
        if regionIn <> None:
            pic = pyautogui.screenshot(region=regionIn)
        else:
            pic = pyautogui.screenshot()

        path = os.path.join(self.root_dir, prefix + '-' + timeStamp + '.png')
        pic.save(path)
        return path        
    
    def do_instructions(self,input):
        #remove after testing
        time.sleep(5)
        #remove after testing
        for instruction in self._GetWorkflow():
            instruc = instruction.split(',')[0]
            params = instruction.split(',')[1:]
            finalParams = []
            for param in params:
                if param == 'd_input':
                    finalParams.append(input)
                else:
                    finalParams.append(param)

            if instruc in self.instructions:
                self.instructions[instruc](finalParams)
            else:
                exit("ERROR, Invalid Instructions")
    
    def DoInstruction(self, instrucName,params):
        if instrucName in self.instructions:
            self.instructions[instrucName](params)
        else:
            exit("ERROR, Invalid Instructions")    

    #x,y
    def process_click(self,params):
        self._GetInteractionService().ProcessClick(params)

    #text
    def process_type(self,params):
        self._GetInteractionService().ProcessType(params[0])

    #text[]
    def process_press(self,params):
        self._GetInteractionService().ProcessPress(params)

    #hotkey[]
    def process_hotkey(self,params):
        self._GetInteractionService().ProcessHotkey(params)
    
    #hotkey[]
    def process_screenshot(self,params):
        pass