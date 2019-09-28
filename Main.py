import src.Managers.Bot as Bot
import src.Container as Container

def run():
    print "Welcome"
    container = Container.Container()
    botManager = container.GetProvider("BotManager")
    botManager.Login()
    botManager.Start()

    
if __name__ == "__main__":
    run()


