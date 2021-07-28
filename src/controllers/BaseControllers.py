from abc import ABC, abstractmethod
import logging
import time
from threading import Thread
from typing import Iterable, Union
from telebot import TeleBot
from telebot.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from telebot.apihelper import ApiTelegramException
from pymorphy2 import MorphAnalyzer
from db.tables.assistant import TaskTable
from db.tables.chat import ChatUserTable, ChatUserModel


appLog: logging.Logger = logging.getLogger("Application")


class BaseController(ABC):

    @abstractmethod
    def initializeMessageHandler(bot: TeleBot) -> None:
        ...

    @staticmethod
    def sendMessage(bot: TeleBot, message: Union[Message, CallbackQuery],  text: str, parseMode: str = None):
        """
        Отправляет сообщение в лс, если боту пишут в группе, и в общий чат, если пишут в лс
        """
        bot.send_message(message.chat.id, text, parse_mode=parseMode) if(
            message.chat.type == 'private') else bot.send_message(message.from_user.id, text, parse_mode=parseMode)

    @staticmethod
    def generateInlineButtons(buttons: Iterable[InlineKeyboardButton]) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        markup.add(*buttons)

        return markup

    @staticmethod
    def getTaskStringTemplate(task: tuple) -> str:
        return (f"<b>Номер заявки:</b> {task.id}" +
                f"\n<b>Организация:</b> {task.orgTitle}" +
                f"\n<b>Статус:</b> {TaskTable.getStatusLabel(task.status)}" +
                f"\n<b>Дата создания:</b> {task.orderDate}" +
                f"\n<b>Устройство:</b> {task.hid} {task.clientTitle}" +
                f"\n<b>Неисправность:</b> {task.descr}")


class ThreadController:

    @staticmethod
    def startTaskDbThreading(bot: TeleBot) -> None:
        """TasksDbThread"""

        # Worker для потока TasksDbThread
        def tasksDbWorker(interval: int = 60):
            appLog.info(f"{tasksDbThread} started")

            while True:
                try:
                    users = ChatUserTable.getUserFields(
                        ChatUserModel.astUserId, ChatUserModel.chatId, filter=[ChatUserModel.isBlocked == False])

                    if(bool(users) is False):
                        continue

                    for user in users:
                        chatId = user['chatId']
                        operatorId = user['astUserId']
                        tasks = TaskTable.getTaskByOperatorId(operatorId)

                        if(bool(tasks) is False):
                            continue

                        morphAnalyzer = MorphAnalyzer()

                        decl1 = morphAnalyzer.parse(
                            'новая')[0].make_agree_with_number(len(tasks)).word

                        decl2 = morphAnalyzer.parse(
                            'заявка')[0].make_agree_with_number(len(tasks)).word

                        headingMessageId = bot.send_message(
                            chatId, f"У вас есть {len(tasks)} {decl1} {decl2}").message_id

                        for task in tasks:
                            bot.send_chat_action(chatId, 'typing')

                            buttons = (InlineKeyboardButton('Принять', callback_data='tasks:|{"id":%s,"status":1, "orgId":%s, "msgId":%s}' % (
                                task.id, task.operatorOrgId, headingMessageId)),)

                            bot.send_message(chatId, BaseController.getTaskStringTemplate(
                                task), parse_mode="html", reply_markup=BaseController.generateInlineButtons(buttons))

                        # Интервал перед итерациями users (имитация задержки в отправке сообщений ботом)
                        time.sleep(len(tasks) + 2)

                    # Интервал между запросами к базе данных
                    time.sleep(interval)

                except ApiTelegramException as error:

                    """ В случае, если не найден чат пользователя, то блокируем его.
                        Это нужно, чтобы цикл while корректно функционировал
                    """
                    if(error.error_code == 400):
                        user = ChatUserTable.getUser(
                            ChatUserModel.astUserId == operatorId)
                        user.isBlocked = True

                        ChatUserTable.updateUser()

                except Exception as error:
                    appLog.exception(error)

        tasksDbThread = Thread(target=tasksDbWorker)
        tasksDbThread.name = "TasksDbThread"
        tasksDbThread.start()
