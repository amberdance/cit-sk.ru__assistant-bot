from abc import ABC, abstractmethod
import logging
from typing import Iterable, List, Union
from sqlalchemy.engine.row import Row
from telebot import TeleBot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from db.storage.assistant import TaskStorage
from db.storage.chat import UserStorage


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
    def generateInlineButtons(buttons: Union[InlineKeyboardButton, Iterable[InlineKeyboardButton]], rowWidth=2) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup(row_width=rowWidth)
        markup.add(*buttons) if isinstance(buttons,
                                           Iterable) else markup.add(buttons)

        return markup

    @staticmethod
    def generateUpdateStatusButtons(taskId: int, chatId: int, statusId: int) -> Union[List, None]:
        isAdmin = UserStorage.isAdmin(chatId)
        buttons = []

        if statusId == 0 and not isAdmin:
            buttons.append(InlineKeyboardButton(
                "Принять", callback_data='tasks:|{"id":%s,"status":1}' % (taskId)))

        elif statusId == 1 and not isAdmin:
            buttons.append(InlineKeyboardButton(
                "Отработать", callback_data='tasks:|{"id":%s,"status":2}' % (taskId)))

        return buttons

    @staticmethod
    def generateTaskHTMLTemlpate(task: Union[tuple, Row]) -> str:
        emoji = {
            0: "❗️",
            1: "❗️",
            2: "✅",
            3: "🚫",
            4: "🚫",
        }

        html = (f"<b>Номер заявки:</b> {task.id} \
                \n<b>Дата создания:</b> {task.orderDate} \
                \n<b>Организация:</b> {task.org}\
                \n<b>Статус:</b> {TaskStorage.getStatusLabel(task.status)} {emoji[task.status]}\
                \n<b>Устройство:</b> {task.hid} {task.client}\
                \n<b>Неисправность:</b> {task.descr}"
                )

        if task.status > 0:
            html += f"\n<b>Оператор:</b> {task.operator or '-'}\n<b>Комментарий:</b> {task.serviceDescr or '-'}"

        return html
