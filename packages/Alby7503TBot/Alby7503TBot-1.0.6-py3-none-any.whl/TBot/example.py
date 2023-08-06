"""example.py"""
from tbot import TBot

BOT = TBot("<token>")
BOT.update_frequence = 0.5  # seconds


@BOT.command("/help")
def help_command(event):
    """Help command handler"""
    BOT.send(event, "Help Message")


@BOT.command("/chat")
def chat(event):
    """Send chat id"""
    group = BOT.get_chat(event)
    if group:
        args = ["title", "type", "id"]
        message = ""
        for i in args:
            message += i.capitalize() + ': ' + str(getattr(group, i)) + "\n"
        BOT.send(event, message)


@BOT.command("*")
def generic(event):
    """Generic command fallback"""
    BOT.send(event, "You said: " + event.text)


BOT.run()
