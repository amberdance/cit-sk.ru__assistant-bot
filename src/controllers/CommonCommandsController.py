from telebot.types import Message
from controllers.BaseControllers import BaseController, TeleBot
from db.tables.chat import ChatUserTable


class CommonCommandsController(BaseController):

    @staticmethod
    def initializeMessageHandler(bot: TeleBot) -> None:
        @bot.message_handler(commands=['help', 'start'])
        def helpCommand(message: Message):

            htmlTemplate = "<b>Справка:</b>\n /userid - id пользователя" + \
                "\n\n <b>Работа с заявками:</b> \n /tasks - список заявок" + \
                "\n /reg - регистрация у бота"

            adminCommands = "\n\n<b>Debug:</b> \n /dbgmsg \n /getme \n /getchat \n /chatid"

            if ChatUserTable.isAdmin(message.from_user.id):
                htmlTemplate += adminCommands

            bot.send_message(
                message.chat.id, parse_mode="html", text=htmlTemplate)
