import re
from typing import List
from telebot import TeleBot
from config import BOT_TOKEN
from .controllers.CommonCommandsController import CommonCommandsController
from .controllers.DatabaseCommandsController import DatabaseCommandsController
from .controllers.ServiceCommandsController import ServiceCommandsController


class PollingBot(CommonCommandsController, DatabaseCommandsController, ServiceCommandsController):

    __telebot: TeleBot = TeleBot(BOT_TOKEN)

    def __init__(self, noneStopPolling: bool = True, interval: int = 0, timeout: int = 20) -> None:
        self.initializeControllers()
        self.__telebot.polling(none_stop=noneStopPolling,
                               interval=interval, timeout=timeout)

    def initializeControllers(self) -> None:
        controllersList: List = PollingBot.mro()

        for controller in controllersList:
            # To do : вписать в regexp
            if controller.__name__ == "BaseController":
                continue

            if re.findall(r"Controller", controller.__name__):
                controller.initializeMessageHandler(self.__telebot)
