import src.Container as Container

def run():
    container = Container.Container()
    container.Logger().debug("Welcome")
    botManager = container.GetProvider("BotManager")
    
    workFlowCommandManager = container.GetProvider("WorkFlowCommandManager")
    workFlowCommandManager.Initialize()

    botManager.Login()
    botManager.Start()
    
if __name__ == "__main__":
    run()


