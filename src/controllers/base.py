from abc import ABC, abstractmethod
import logging
from typing import Iterable
from telebot import TeleBot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from db.storage.assistant import TaskStorage


appLog: logging.Logger = logging.getLogger("Application")


class BaseController(ABC):
    _bot = None

    def __init__(self, bot: TeleBot) -> None:
        self._bot = bot

    @abstractmethod
    def initialize() -> None: ...

    @staticmethod
    def isPublicChat(message: Message) -> bool:
        return True if message.chat.type == 'group' else False

    @staticmethod
    def generateInlineButtons(buttons: Iterable[InlineKeyboardButton]) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        markup.add(*buttons)

        return markup

    @staticmethod
    def getTaskStringTemplate(task: tuple) -> str:
        return (f"<b>Номер заявки:</b> {task.id}" +
                f"\n<b>Организация:</b> {task.org}" +
                f"\n<b>Статус:</b> {TaskStorage.getStatusLabel(task.status)}" +
                f"\n<b>Дата создания:</b> {task.orderDate}" +
                f"\n<b>Устройство:</b> {task.hid} {task.client}" +
                f"\n<b>Неисправность:</b> {task.descr}")
