import pyautogui
import os 
from datetime import datetime
import time

#remove after testing
#pyautogui.PAUSE = 1.5
#remove after testing

class ScreenHelper(object):
    def __init__(self,container):
        config = container.GetProvider("Configuration")
   
        self.root_dir = self.create_year_directory()
        self.workflow = config.instructions
        self.instructions = {
            "click" : self.process_click,
            "type" : self.process_type,
            "press" : self.process_press
        }
    
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

    def save_screen_with_timestamp(self,prefix):
        self.do_instructions(prefix)

        timeStamp = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
        pic = pyautogui.screenshot()
        path = os.path.join(self.root_dir, prefix + '-' + timeStamp + '.png')
        pic.save(path)
        return path
    
    def do_instructions(self,input):
        #remove after testing
        time.sleep(5)
        #remove after testing
        for instruction in self.workflow:
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

    #x,y
    def process_click(self,params):
        print "clicking " + str(params)
        pyautogui.click(int(params[0]),int(params[1]))

    #text
    def process_type(self,params):
        print "typing " + str(params)
        pyautogui.typewrite(params[0])

    #text[]
    def process_press(self,params):
        print "pressing  " + str(params)
        pyautogui.typewrite(params)
    