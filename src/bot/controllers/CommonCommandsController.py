from telebot import TeleBot
from .BaseController import BaseController


class CommonCommandsController(BaseController):

    @staticmethod
    def initializeMessageHandler(bot: TeleBot) -> None:
        @bot.message_handler(commands=['help'])
        def helpCommand(message):
            bot.send_message(message.chat.id, "help here")
