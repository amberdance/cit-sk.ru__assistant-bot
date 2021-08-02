from telebot.types import Message
from controllers.base import BaseController, TeleBot


class CommonCommandsController(BaseController):
    def __init__(self, bot: TeleBot) -> None:
        super().__init__(bot)

    def initialize(self) -> None:
        @self._bot.message_handler(['help', 'start'])
        def helpCommand(message: Message):

            htmlTemplate = "<b>Пользователь:</b>" \
                "\n/reg - регистрация нового пользователя" \
                "\n /userid - id пользователя"  \
                "\n\n<b>Работа с заявками:</b>" \
                "\n/tasks - новые заявки" \
                "\n/tasks-1 - принятые заявки" \
                "\n\n<b>Общее:</b>" \
                "\n/cancel - отмена текущей команды"

            self._bot.send_message(
                message.chat.id, htmlTemplate, parse_mode="html")
