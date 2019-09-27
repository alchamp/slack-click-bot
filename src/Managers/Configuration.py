import os

class Configuration(object):
    def __init__(self):
        self.config_file_path = os.path.join(os.getcwd(), "bot.config")
        #Read config file
        with open(self.config_file_path) as f:
            content = f.readlines()
        content = [x.strip() for x in content] 
        self.bot_token = content[0]
        self.bot_name = content[1]
        self.instructions = content[2:]