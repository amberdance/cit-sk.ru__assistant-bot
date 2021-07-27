from pprint import pformat
from telebot import TeleBot
from controllers.BaseControllers import BaseController, Message


class ServiceCommandsController(BaseController):

    @staticmethod
    def initializeMessageHandler(bot: TeleBot) -> None:
        @bot.message_handler(commands=['userid'])
        def getUserIdCommand(message: Message) -> None:
            bot.reply_to(message, f'Ваш ID: {message.from_user.id}')
            # BaseController.sendMessage(
            #     bot, message, f'Ваш ID: {message.from_user.id}')
