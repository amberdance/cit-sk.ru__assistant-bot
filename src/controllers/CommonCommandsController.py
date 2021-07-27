from telebot.types import Message
from controllers.BaseControllers import BaseController, TeleBot


class CommonCommandsController(BaseController):

    @staticmethod
    def initializeMessageHandler(bot: TeleBot) -> None:
        @bot.message_handler(commands=['help', 'start'])
        def helpCommand(message: Message):

            htmlTemplate = "<b>Справка:</b>\n /userid - id пользователя" + \
                "\n/tasks - список заявок" + \
                "\n<b>Работа с заявками:</b>" +\
                "\n/reg - регистрация нового пользователя"

            bot.send_message(
                message.chat.id, htmlTemplate, parse_mode="html")
