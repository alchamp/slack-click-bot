import time
import random
class WorkflowExecutor(object):
    def __init__(self,container):
        self._container = container
        self.instructions = {
            "click" : self.execute_click,
            "type" : self.execute_type,
            "press" : self.execute_press,
            "hotkey" : self.execute_hotkey,
            "screenshot":self.execute_screenshot
        }

    def GetWorkFlowCommandManager(self):
        return self._container.GetProvider("WorkFlowCommandManager")
    def GetScreenHelper(self):
        return self._container.GetProvider("ScreenHelper")   
    def GetInteractionService(self):
        return self._container.GetProvider("InteractionService")
    def GetWindowManager(self):
        return self._container.GetProvider("WindowManager")
    def GetOsService(self):
        return self._container.GetProvider("OsService")     
    def GetBotService(self):
        return self._container.GetProvider("BotService")

    def Execute(self,slackCommandName,inputs,channel,user):
        #remove after testing
        time.sleep(1)
        workflows = self.GetWorkFlowCommandManager().GetCommandWorkFlows(slackCommandName)
        for workflow in workflows:
            self.ExecuteWorkFlow(workflow,inputs,channel,user) 

    def ExecuteWorkFlow(self,workflowModel,inputs,channel,user):
        #get window
        osHandlerModel = self.GetWindowModel(workflowModel.windowname)

        #bring window forward
        if osHandlerModel:
            self.GetWindowManager().BringForward(osHandlerModel)

        #execute instruction
        for commandModel in workflowModel.commands:
            self.ExecuteInstruction(commandModel,inputs,channel,user,osHandlerModel)
        pass

    def GetWindowModel(self,name):
            self.GetOsService().PopulateWindowsEnumChild(1)
            model = self.GetOsService().GetWindowByName(name, 1)

            return model
    def ParamsSubInputs(self,params,inputs):
        finalParams = []
        for param in params:
            if param == 'd_input0':
                finalParams.append(inputs[0])
            elif param == 'd_input1':
                finalParams.append(inputs[1])          
            elif param == 'd_input2':
                finalParams.append(inputs[2])                                   
            else:
                finalParams.append(str(param))
        return finalParams

    def ExecuteInstruction(self, commandModel,inputs,channel,user,osHandlerModel):
        finalParams = self.ParamsSubInputs(commandModel.params,inputs)
        if commandModel.command in self.instructions:
            self.instructions[commandModel.command](finalParams,osHandlerModel,channel,user)
        else:
            exit("ERROR, Invalid Instructions")  
 
    #x,y
    def execute_click(self,params,osHandlerModel,channel,user):
        windowPoint = self.GetWindowManager().GetWindowPointToScreen(osHandlerModel, int(params[0]),int(params[1]))
        self.GetInteractionService().ProcessClick(windowPoint)

    #text
    def execute_type(self,params,osHandlerModel,channel,user):
        self.GetInteractionService().ProcessType(params)

    #text[]
    def execute_press(self,params,osHandlerModel,channel,user):
        self.GetInteractionService().ProcessPress(params)

    #hotkey[]
    def execute_hotkey(self,params,osHandlerModel,channel,user):
        self.GetInteractionService().ProcessHotkey(params)
    
    #hotkey[]
    def execute_screenshot(self,params,osHandlerModel,channel,user):
        screenshot = self.GetScreenHelper().realSaveScreen("image" +str(random.randint(0,1000)), self.GetWindowManager().GetLeftTopWidthHeight(osHandlerModel))
        self.GetBotService().UploadFile(channel, '',screenshot)