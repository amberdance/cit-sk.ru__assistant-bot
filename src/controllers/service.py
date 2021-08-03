from telebot.types import BotCommand
from controllers.base import BaseController, Message, TeleBot


class ServiceCommandsController(BaseController):
    def __init__(self, bot: TeleBot) -> None:
        super().__init__(bot)
        self.registerBotCommands()

    def initialize(self) -> None:
        @self._bot.message_handler(['userid'])
        def getModelIdCommand(message: Message) -> None:
            self._bot.reply_to(message, f'Ваш Id: {message.from_user.id}')

    def registerBotCommands(self) -> None:
        self._bot.set_my_commands([
            BotCommand("help", "справка"),
            BotCommand("reg", "регистрация пользователя"),
            BotCommand("userid", "user id"),
            BotCommand("tasks", "работа с заявками"),
            BotCommand("cancel", "отмена текущего действия"),
        ])
