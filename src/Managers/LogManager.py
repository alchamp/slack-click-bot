from logging import StreamHandler
import logging

class SlackLogHandler(StreamHandler):
    def __init__(self,container):
        StreamHandler.__init__(self)
        self._container = container

    def GetBotService(self):
        return self._container.GetProvider("BotService")
    def GetBotManager(self):
        return self._container.GetProvider("BotManager")

    def emit(self, record):
        if self.GetBotManager().IsRunning() and self.GetBotService().IsReady() and self.GetBotService().GetLoggingChannelId() <> None:
            msg = self.format(record)
            self.GetBotService().PostTextMessage(None,self.GetBotService().GetLoggingChannelId(),msg)

class LogManager(object):
    def __init__(self,container):
        self._container = container
        logging.basicConfig(
            format='%(asctime)s %(levelname)s %(message)s', 
            level=logging.DEBUG, 
            datefmt='%m/%d/%Y %I:%M:%S %p'
            )
        self.logger = logging.getLogger('Bot Logger')

        slacklogger = SlackLogHandler(container)
        slacklogger.setLevel(logging.ERROR)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        slacklogger.setFormatter(formatter)
        self.logger.addHandler(slacklogger)

    def GetLogger(self):
        return self.logger