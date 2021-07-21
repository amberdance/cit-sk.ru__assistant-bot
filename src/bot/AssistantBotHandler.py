from telebot import TeleBot
from config import BOT_TOKEN
from db.AssistantDbContext import AssistantDbContext
from .commands.CommonCommands import CommonCommands
from .commands.DatabaseCommands import DatabaseCommands
from .commands.ServiceCommands import ServiceCommands


class AssistantBotHandler(AssistantDbContext, CommonCommands, DatabaseCommands):

    __telebot = None
    __assistantDatabase = None

    def __init__(self,  noneStopPolling=True, interval=0, timeout=20):
        self.__telebot = TeleBot(BOT_TOKEN)
        # self.__assistantDatabase = AssistantDbContext()

        self.initializeCommandsListener()
        self.__telebot.polling(none_stop=noneStopPolling,
                               interval=interval, timeout=timeout)

    def initializeCommandsListener(self):
        CommonCommands.initializeMessageHandler(self.__telebot)
        ServiceCommands.initializeMessageHandler(self.__telebot)
        DatabaseCommands.initializeMessageHandler(
            self.__telebot, self.__assistantDatabase)
