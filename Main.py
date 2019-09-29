import src.Container as Container

def run():
    print "Welcome"
    container = Container.Container()
    botManager = container.GetProvider("BotManager")
    
    workFlowCommandManager = container.GetProvider("WorkFlowCommandManager")
    workFlowCommandManager.Initialize()

    botManager.Login()
    botManager.Start()

    
if __name__ == "__main__":
    run()


