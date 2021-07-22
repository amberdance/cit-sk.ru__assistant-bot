from .BaseController import BaseController
from telebot import TeleBot


class ServiceCommandsController(BaseController):

    @staticmethod
    def initializeMessageHandler(bot: TeleBot) -> None:
        @bot.message_handler(commands=['userid'])
        def getUserIdCommand(message) -> None:
            bot.reply_to(
                message, f'Ваш ID: {message.from_user.id}')
