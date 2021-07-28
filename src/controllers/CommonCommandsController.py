from telebot.types import Message
from controllers.BaseControllers import BaseController, TeleBot


class CommonCommandsController(BaseController):

    @staticmethod
    def initializeMessageHandler(bot: TeleBot) -> None:
        @bot.message_handler(commands=['help', 'start'])
        def helpCommand(message: Message):

            htmlTemplate = "<b>Пользователь:</b>" \
                "\n/reg - регистрация нового пользователя" \
                "\n /userid - id пользователя"  \
                "\n\n<b>Работа с заявками:</b>" \
                "\n/tasks - список заявок:" \
                "\n/tasks-1 - принятые в работу заявки"\
                "\n/tasks-2 - отработанные заявки" \
                "\n/tasks-3 - отмененные заявки" \
                "\n/tasks-4 - отклоненные заявки"\


            bot.send_message(
                message.chat.id, htmlTemplate, parse_mode="html")
