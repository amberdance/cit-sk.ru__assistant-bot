from bot.commands.taskmenu import TaskMenuHandler
from .base import BaseController, TeleBot
from bot.commands import *
from src.config import DEBUG_MODE


class DatabaseCommandsController(BaseController):

    def __init__(self, bot: TeleBot) -> None:
        super().__init__(bot)

    def initialize(self) -> None:
        if (DEBUG_MODE == False):
            TaskHandler.scanningTasks(self._bot, 180)
        TaskHandler.initialize(self._bot)
        TaskMenuHandler(self._bot)
        ChatUserHandler.initialize(self._bot)
