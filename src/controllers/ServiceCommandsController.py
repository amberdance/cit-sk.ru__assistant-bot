from pprint import pformat
from telebot import TeleBot
from telebot.types import BotCommand
from controllers.BaseControllers import BaseController, Message


class ServiceCommandsController(BaseController):

    @staticmethod
    def initializeMessageHandler(bot: TeleBot) -> None:
        @bot.message_handler(commands=['userid'])
        def getUserIdCommand(message: Message) -> None:
            bot.reply_to(message, f'Ваш ID: {message.from_user.id}')

        def registerBotCommands() -> None:
            bot.set_my_commands([
                BotCommand("help", "справка"),
                BotCommand("reg", "регистрация пользователя"),
                BotCommand("userid", "узнать мой Id"),
                BotCommand("tasks", "новые заявки"),
            ])
