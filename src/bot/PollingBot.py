import logging
import telebot
from telebot import TeleBot
from config import BOT_TOKEN
from controllers import CommonCommandsController, DatabaseCommandsController, ServiceCommandsController


class PollingBot():

    __telebot: TeleBot = TeleBot(BOT_TOKEN)

    def __init__(self, noneStopPolling: bool = True, logLevel=logging.ERROR, interval: int = 0, timeout: int = 20) -> None:
        logger = logging.getLogger('Application')
        telebot.logger.setLevel(logLevel)

        self.initializeControllers()

        logger.info("PollingBot initialized")

        self.__telebot.polling(none_stop=noneStopPolling,
                               interval=interval, timeout=timeout)

    def initializeControllers(self) -> None:
        controllers = (CommonCommandsController,
                       ServiceCommandsController, DatabaseCommandsController)

        for obj in controllers:
            obj.initializeMessageHandler(self.__telebot)
