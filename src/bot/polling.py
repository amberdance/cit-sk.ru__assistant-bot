import logging
import telebot
from config import BOT_TOKEN
from controllers import DatabaseCommandsController, CommonCommandsController, ServiceCommandsController


class PollingBot():

    def __init__(self, noneStopPolling: bool = True, logLevel=logging.ERROR, interval: int = 0, timeout: int = 20) -> None:
        logger = logging.getLogger('Application')
        bot = telebot.TeleBot(BOT_TOKEN)

        telebot.logger.setLevel(logLevel)

        controllers = (CommonCommandsController,
                       ServiceCommandsController,
                       DatabaseCommandsController,)

        for controller in controllers:
            controller(bot).initialize()

        logger.info("Polling Bot started")

        bot.polling(none_stop=noneStopPolling,
                    interval=interval, timeout=timeout)
