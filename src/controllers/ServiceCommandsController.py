from pprint import pformat
from telebot import TeleBot
from controllers.BaseControllers import BaseController, Message


class ServiceCommandsController(BaseController):

    @staticmethod
    def initializeMessageHandler(bot: TeleBot) -> None:
        @bot.message_handler(commands=['userid'])
        def getUserIdCommand(message) -> None:
            bot.reply_to(message, f'Ваш ID: {message.from_user.id}')
            # BaseController.sendMessage(
            #     bot, message, f'Ваш ID: {message.from_user.id}')

        @ bot.message_handler(commands=['chatid'])
        def debugMessage(message: Message):
            BaseController.sendMessage(
                bot, message, message.chat.id)

        @ bot.message_handler(commands=['dbgmsg'])
        def debugMessage(message: Message):
            BaseController.sendMessage(
                bot, message, message)

        @ bot.message_handler(commands=['getme'])
        def debugMessage(message: Message):
            BaseController.sendMessage(bot, message, bot.get_me())

        @ bot.message_handler(commands=['getchat'])
        def debugMessage(message: Message):
            BaseController.sendMessage(
                bot, message, pformat(bot.get_chat(message.chat.id).__dict__))
