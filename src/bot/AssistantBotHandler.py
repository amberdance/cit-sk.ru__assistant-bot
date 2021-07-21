from telebot import TeleBot
from config import BOT_TOKEN
from .controllers.CommonCommandsController import CommonCommandsController
from .controllers.DatabaseCommandsController import DatabaseCommandsController
from .controllers.ServiceCommandsController import ServiceCommandsController


class AssistantBotHandler(CommonCommandsController, DatabaseCommandsController, ServiceCommandsController):

    __telebot: TeleBot = None
    # To do: проработать вопрос с контекстами бд
    __assistantDbCntext = None
    __telegramDbContext = None

    def __init__(self,  noneStopPolling: bool = True, interval: int = 0, timeout: int = 20) -> None:
        self.__telebot = TeleBot(BOT_TOKEN)

        self.initializeControllers()
        self.__telebot.polling(none_stop=noneStopPolling,
                               interval=interval, timeout=timeout)

    def initializeControllers(self) -> None:
        # To do: обернуть в цикл
        CommonCommandsController.initializeMessageHandler(self.__telebot)
        ServiceCommandsController.initializeMessageHandler(self.__telebot)
        DatabaseCommandsController.initializeMessageHandler(
            self.__telebot, self.__assistantDbCntext)
