from pprint import pformat
from telebot import TeleBot
from .BaseController import BaseController


class ServiceCommandsController(BaseController):

    @staticmethod
    def initializeMessageHandler(bot: TeleBot) -> None:
        @bot.message_handler(commands=['userid'])
        def getUserIdCommand(message) -> None:
            BaseController.sendMessage(
                bot, message, f'Ваш ID: {message.from_user.id}')

        @bot.message_handler(commands=['dbgmsg'])
        def debugMessage(message):
            BaseController.sendMessage(
                bot, message, message)

        @bot.message_handler(commands=['getme'])
        def debugMessage(message):
            BaseController.sendMessage(bot, message, bot.get_me())

        @bot.message_handler(commands=['getchat'])
        def debugMessage(message):
            BaseController.sendMessage(
                bot, message, pformat(bot.get_chat(message.chat.id).__dict__))
