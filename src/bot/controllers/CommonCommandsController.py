from telebot.types import Message
from .BaseController import BaseController, TeleBot
from db.tables.ChatUserTable import ChatUserTable, ChatUserModel


class CommonCommandsController(BaseController):

    @staticmethod
    def initializeMessageHandler(bot: TeleBot) -> None:
        @bot.message_handler(commands=['help'])
        def helpCommand(message: Message):

            htmlTemplate = "<b>Справка</b>\n /userid - id пользователя" + \
                "\n\n <b>Работа с заявками</b> \n /task - информация о заявке по ее номеру"

            adminCommands = "\n\n<b>Debug</b> \n /dbgmsg \n /getme \n /getchat"

            if ChatUserTable.isAdmin(message.from_user.id):
                htmlTemplate += adminCommands

            bot.send_message(
                message.chat.id, parse_mode="html", text=htmlTemplate)
