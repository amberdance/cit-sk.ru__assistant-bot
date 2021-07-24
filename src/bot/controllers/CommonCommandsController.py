from telebot.types import Message
from .BaseController import BaseController, TeleBot
from db.tables.chat import UserTable


class CommonCommandsController(BaseController):

    @staticmethod
    def initializeMessageHandler(bot: TeleBot) -> None:
        @bot.message_handler(commands=['help'])
        def helpCommand(message: Message):

            htmlTemplate = "<b>Справка</b>\n /userid - id пользователя" + \
                "\n\n <b>Работа с заявками</b> \n /task - информация о заявке по ее номеру \n /reg - регистрация у бота"

            adminCommands = "\n\n<b>Debug</b> \n /dbgmsg \n /getme \n /getchat"

            if UserTable.isAdmin(message.from_user.id):
                htmlTemplate += adminCommands

            bot.send_message(
                message.chat.id, parse_mode="html", text=htmlTemplate)
