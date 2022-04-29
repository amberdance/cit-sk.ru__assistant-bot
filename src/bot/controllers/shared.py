from telebot.types import Message
from db.storage.chat import UserStorage
from .base import BaseController, TeleBot


class CommonCommandsController(BaseController):
    def __init__(self, bot: TeleBot) -> None:
        super().__init__(bot)

    def initialize(self) -> None:
        @self._bot.message_handler(['help', 'start'])
        def helpCommand(message: Message):
            if self.isPublicChat(message):
                return

            baseCommands = (
                "/reg - регистрация нового пользователя",
                "/userid - id пользователя",
                "/tasks - заявки",
                "/cancel - отмена текущей команды",
                "/subscribe - подписка на рассылку",
                "/unsubscribe - отписаться от рассылки",

            )

            adminCommands = (
                "/purgeusr - удалить заблокированных пользователей",
            )

            result = "\n".join(baseCommands) + "\n" + "\n".join(adminCommands) if UserStorage.isAdmin(
                message.chat.id) else "\n".join(baseCommands)

            self._bot.send_message(message.chat.id, result)
