import src.Managers.Bot as Bot
import src.Container as Container

def run():
    print "Welcome"
    container = Container.Container()
    bot = Bot.Bot(container)
    bot.start_listening_for_events()
if __name__ == "__main__":
    run()


