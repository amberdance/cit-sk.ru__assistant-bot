from controllers.base import BaseController, TeleBot
from bot.commands import *


class DatabaseCommandsController(BaseController):

    def __init__(self, bot: TeleBot) -> None:
        super().__init__(bot)

    def initialize(self) -> None:
        TaskHandler.scanningTasks(self._bot, 90)
        ChatUserHandler.initialize(self._bot)
        TaskHandler.initialize(self._bot)
