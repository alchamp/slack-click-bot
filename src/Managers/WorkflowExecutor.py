import time
import random

class WorkflowExecutor(object):
    def __init__(self,container):
        self._container = container
        self.instructions = {
            "click" : self.execute_click,
            "doubleclick" : self.execute_doubleclick,
            "type" : self.execute_type,
            "press" : self.execute_press,
            "hotkey" : self.execute_hotkey,
            "onscreenkey" : self.execute_on_screen_key,
            "screenshot":self.execute_screenshot,
            "delay":self.execute_delay
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
    def GetConfiguration(self):
        return self._container.GetProvider("Configuration")
    def GetOnScreenKeyboardManager(self):
        return self._container.GetProvider("OnScreenKeyboardManager")

    def Execute(self,slackCommandName,inputs,channel,user):
        workflows = self.GetWorkFlowCommandManager().GetCommandWorkFlows(slackCommandName)
        for workflow in workflows:
            self.ExecuteWorkFlow(workflow,inputs,channel,user) 

    def ExecuteWorkFlow(self,workflowModel,inputs,channel,user):
        #get window
        osHandlerModel = self.GetWindowModel(workflowModel.windowname,workflowModel.excludednames)
        if osHandlerModel == None:
            if workflowModel.program <> None:
                success = self.GetOsService().StartProgram(workflowModel.program)
                if success:
                    if workflowModel.programdelay <> None:
                        messageOut = " Attempting To Start `" + str(workflowModel.program) + "` Sleeping For `" + str(workflowModel.programdelay) + "` Seconds"
                        self.GetBotService().PostTextMessage(user,channel, messageOut)
                        time.sleep(workflowModel.programdelay)
                    #get window
                    osHandlerModel = self.GetWindowModel(workflowModel.windowname,workflowModel.excludednames)  
        
        #bring window forward
        if osHandlerModel:
            self.GetWindowManager().BringForward(osHandlerModel)
            if self.GetConfiguration().ShouldMaximizeWindows():
                time.sleep(.5)
                self.GetWindowManager().Maximize(osHandlerModel)

            #execute instruction
            for commandModel in workflowModel.commands:
                self.ExecuteInstruction(commandModel,inputs,channel,user,osHandlerModel,workflowModel)
        else:
            messageOut = " Could Not Find `" + str(workflowModel.windowname) + "` Skipping Workflow `" +  str(workflowModel.name) + "`"
            self.GetBotService().PostTextMessage(user,channel, messageOut) 

    def GetWindowModel(self,name,exNames):
            self.GetOsService().PopulateWindowsEnumChild(1)
            model = self.GetOsService().GetWindowByName(name, 1,exNames)

            return model
    def ParamsSubInputs(self,params,inputs):
        finalParams = []
        for param in params:
            dinputSet = False
            for i in range(20):
                if param == ('d_input'+str(i)):
                    finalParams.append(inputs[i])
                    dinputSet = True
                    break                             
            if(dinputSet == False):
                finalParams.append(str(param))
        return finalParams

    def ExecuteInstruction(self, commandModel,inputs,channel,user,osHandlerModel,workflowModel = None):
        if commandModel.command in self.instructions:
            finalParams = self.ParamsSubInputs(commandModel.params,inputs)
            self.instructions[commandModel.command](finalParams,osHandlerModel,channel,user,workflowModel)
        else:
            self._container.Logger().error("invalid instruction " + commandModel.command)
            raise Exception("ERROR, Invalid Instructions")  
 
    def _GetWidthHeightFactor(self,osHandlerModel,workflowModel):
        widthFactor = 1.0
        heightFactor = 1.0   
        if workflowModel <> None:
            origW = workflowModel.originalwidth
            origH = workflowModel.originalheight
            if (origW <> None) and (origH <> None) and (origW > 0) and (origH > 0) :      
                (wf, hf) = self.GetWindowManager().GetInterpolatedRatio(osHandlerModel,origW,origH)
                widthFactor = wf
                heightFactor = hf
                self._container.Logger().info(" Workflow Exec: WidthFactor: " + str(widthFactor) + " heightFactor: " + str(heightFactor))
        return (widthFactor,heightFactor)

    def _GetPoint(self, params,osHandlerModel,workflowModel):
        if self.GetConfiguration().GetInterpolateClicks() == False or workflowModel == None:
            return self.GetWindowManager().GetWindowPointToScreen(osHandlerModel, int(params[0]),int(params[1]))
        else:
            (widthFactor,heightFactor) = self._GetWidthHeightFactor(osHandlerModel,workflowModel)
            (x,y) = self.GetWindowManager().GetWindowPointToScreenInterpolatedWithFactors(osHandlerModel,int(params[0]),int(params[1]),widthFactor,heightFactor)
            return(x,y)

    #x,y
    def execute_click(self,params,osHandlerModel,channel,user,workflowModel = None):
        windowPoint = self._GetPoint(params,osHandlerModel, workflowModel)
        self.GetInteractionService().ProcessClick(windowPoint)
    #x,y
    def execute_doubleclick(self,params,osHandlerModel,channel,user,workflowModel = None):
        windowPoint = self._GetPoint(params,osHandlerModel, workflowModel)
        self.GetInteractionService().ProcessDoubleClick(windowPoint)
    #text
    def execute_type(self,params,osHandlerModel,channel,user,workflowModel = None):
        self.GetInteractionService().ProcessType(params)

    #text[]
    def execute_press(self,params,osHandlerModel,channel,user,workflowModel = None):
        self.GetInteractionService().ProcessPress(params)

    #hotkey[]
    def execute_hotkey(self,params,osHandlerModel,channel,user,workflowModel = None):
        self.GetInteractionService().ProcessHotkey(params)

    #hotkey[]
    def execute_on_screen_key(self,params,osHandlerModel,channel,user,workflowModel = None):
        if( self.GetOnScreenKeyboardManager().IsEnabled()):
            if(self.GetOnScreenKeyboardManager().HasAllKeyAvailable(params)):
                self.GetOnScreenKeyboardManager().ClickAvailableKeys(params)
            else:
                self._container.Logger().error("On Screen Keyboard Feature Does Not Support Some Keys" + str(params))
                raise Exception("On Screen Keyboard Feature Does Not Support Some Keys" + str(params))  
        else:
            self._container.Logger().error("On Screen Keyboard Feature Not  Available")
            raise Exception("On Screen Keyboard Feature Not  Available")

    #screenshot[]
    def execute_screenshot(self,params,osHandlerModel,channel,user,workflowModel = None):
        screenshot = self.GetScreenHelper().realSaveScreen("image" +str(random.randint(0,1000)), self.GetWindowManager().GetLeftTopWidthHeight(osHandlerModel))
        self.GetBotService().UploadFile(channel, '',screenshot)

    #sleep,seconds
    def execute_delay(self,params,osHandlerModel,channel,user,workflowModel = None):
        self.GetOsService().Sleep(float(params[0]))

