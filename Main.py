import Bot
import Container

def run():
    print "Welcome"
    container = Container.Container()
    bot = Bot.Bot(container)
    bot.start_listening_for_events()
    
if __name__ == "__main__":
    run()


