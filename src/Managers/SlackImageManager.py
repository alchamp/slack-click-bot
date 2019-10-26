import threading
import Queue
import datetime
import time

class SlackImageManager(threading.Thread):
    def __init__(self,container):
        self._running = False
        self._currentTimer = None
        self._currentId = -1
        self._currentCount = 0        
        self._container = container
        self._imageQueue = Queue.Queue()
        threading.Thread.__init__(self)

    def GetBotService(self):
        return self._container.GetProvider("BotService")
    def GetOsService(self):
        return self._container.GetProvider("OsService")     
    def GetConfigManager(self):
        return self._container.GetProvider("Configuration")


    def AddImageToQueue(self, queueInput):
        self._imageQueue.put(queueInput)

    def ProcessQueue(self):
        qItem = self._imageQueue.get()
        imageSetId = qItem[1]
        isEnd = qItem[0] == "END"
        channel = qItem[2] 
        user = qItem[3] 

        if self._currentId != imageSetId:
            self._currentTimer = datetime.datetime.now()
            self._currentId = imageSetId
            self._currentCount = 0

        if isEnd:
            elsapsedTime = datetime.datetime.now() - self._currentTimer
            message = "Done Proccessing Screenshots For Command #" + str(self._currentId) + " # of Screenshots " + str(self._currentCount) + " Execution Time: " + str(elsapsedTime) 
            self.GetBotService().PostTextMessage(user, channel,message)            
        else:
            self._currentCount += 1
            screenshot = qItem[4]
            self.GetBotService().UploadFile(channel, '',screenshot)            

    def Start(self):
        if  self.GetConfigManager().UseImageThread() and self._running == False:
            self._container.Logger().info("Starting Image Thread")
            self._running = True
            return self.start()
        else:
            self._container.Logger().info("Not Starting Image Thread")

    def Stop(self):
        self._running = False

    def IsRunning(self):
        return self._running

    def run(self):
        while self._running:
            try:
                while not self._imageQueue.empty():
                    self.ProcessQueue()
            except Exception as error:                                       
                try:
                    self._container.Logger().exception(error)
                except:
                    pass
                if not self.GetConfigManager().GetAlwaysOn():
                    raise
            time.sleep(.1)