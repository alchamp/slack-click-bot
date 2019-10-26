import time
import random
from datetime import datetime

class WorkflowExecutor(object):
    def __init__(self,container):
        self._command_counter = 0
        self._container = container
        self.instructions = {
            "click" : self.execute_click,
            "doubleclick" : self.execute_doubleclick,
            "type" : self.execute_type,
            "press" : self.execute_press,
            "hotkey" : self.execute_hotkey,
            "onscreenkey" : self.execute_on_screen_key,
            "screenshot":self.execute_screenshot,
            "delay":self.execute_delay,
            "optionalsplitlocation":self.execute_no_op
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
    def GetSlackImageManager(self):
        return self._container.GetProvider("SlackImageManager")

    def Execute(self,slackCommandName,inputs,channel,user):
        self._command_counter += 1
        workflows = self.GetWorkFlowCommandManager().GetCommandWorkFlows(slackCommandName)
        for workflow in workflows:
            self.ExecuteWorkFlow(workflow,inputs,channel,user)

        if(self.GetSlackImageManager().IsRunning()):
            self.GetSlackImageManager().AddImageToQueue(("END",self._command_counter,channel,user,None))

        return  self._command_counter

    def ExecuteWorkFlow(self,workflowModel,inputs,channel,user):
        #get window
        startTime = datetime.now()
        osHandlerModel = self.GetWindowModel(workflowModel.windowname,workflowModel.excludednames)
        self._container.Logger().debug("***GetWindowModel Time: " + str(datetime.now() - startTime))

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
            optionalInput = self.FindOptionalInputIndex(workflowModel.commands)
            commandSplit = self.SplitCommands(workflowModel.commands,optionalInput)
            startTime = datetime.now()
            for commandModel in commandSplit[0]:
                startTime1 = datetime.now()
                self.ExecuteInstruction(commandModel,inputs,channel,user,osHandlerModel,workflowModel)
                self._container.Logger().debug("***" + str(commandModel) + "\n\t\t\t\tTime: " +  str(datetime.now() - startTime1))

            self._container.Logger().debug("***ExecuteInstruction Time: " + str(len(commandSplit[0])) + " " + str(datetime.now() - startTime))

            startTime = datetime.now()             
            for input in inputs:                
                for commandModel in commandSplit[1]:
                    self.ExecuteInstruction(commandModel,[input],channel,user,osHandlerModel,workflowModel)     
            self._container.Logger().debug("***Split ExecuteInstruction Time: " + str(datetime.now() - startTime))
        else:
            messageOut = " Could Not Find `" + str(workflowModel.windowname) + "` Skipping Workflow `" +  str(workflowModel.name) + "`"
            self.GetBotService().PostTextMessage(user,channel, messageOut) 

    def GetWindowModel(self,name,exNames):
            startTime = datetime.now()
            self.GetOsService().PopulateWindowsEnumChild(1)
            self._container.Logger().debug("***PopulateWindowsEnumChild Time: " + str(datetime.now() - startTime))
            startTime = datetime.now()        
            model = self.GetOsService().GetWindowByName(name, 1,exNames)
            self._container.Logger().debug("***GetWindowByName Time: " + str(datetime.now() - startTime))            
            return model

    def FindOptionalInputIndex(self,commands):
        found = None
        idx = 0
        for commandModel in commands: 
            if commandModel.command == ('optionalsplitlocation'):
                found = idx
                self._container.Logger().info(" Found optional split location at " + str(idx))
                break               
            idx = idx + 1
        return found   

    def SplitCommands(self,commands,index):
        if index == None:
            self._container.Logger().info("No Splitting commands ")
            return (commands, [])
        else:
            self._container.Logger().info(" Splitting commands at index " + str(index))
            return (commands[0:index],commands[index:])
        
    def ParamsSubInputs(self,params,inputs):
        finalParams = []
        for param in params:
            dinputSet = False
            for i in range(10):
                if param == ('o_input'):
                    finalParams.append(inputs[0])
                    dinputSet = True
                    break
                    
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
        if self.GetConfiguration().ShouldInterpolateClicks() == False or workflowModel == None:
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
        if(self.GetSlackImageManager().IsRunning()):
            self.GetSlackImageManager().AddImageToQueue(("Image",self._command_counter,channel,user,screenshot))
        else:
            self.GetBotService().UploadFile(channel, '',screenshot)

    #sleep,seconds
    def execute_delay(self,params,osHandlerModel,channel,user,workflowModel = None):
        self.GetOsService().Sleep(float(params[0]))
        
    #no_op
    def execute_no_op(self,params,osHandlerModel,channel,user,workflowModel = None):
        pass
