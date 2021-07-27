from abc import ABC, abstractmethod
import logging
import time
from threading import Thread
from typing import Iterable, Union
from telebot import TeleBot
from telebot.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
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
                f"\n<b>Дата создания:</b> {task.orderDate}" +
                f"\n<b>Устройство:</b> {task.hid} {task.clientTitle}" +
                f"\n<b>Неисправность:</b> {task.descr}")


class ThreadController:

    @staticmethod
    def startTaskDbThreading(bot: TeleBot) -> None:
        """TasksDbThread"""

        # Worker для потока TasksDbThread
        def tasksDbWorker(interval: int = 300):
            appLog.info(f"{tasksDbThread.name} was started")

            while True:
                try:
                    subscribers = ChatUserTable.getUserFields(
                        ChatUserModel.username, ChatUserModel.chatUserId, filter=[ChatUserModel.chatUserId == 686739701, ChatUserModel.isBlocked == False])

                    for user in subscribers:
                        chatId = user['chatUserId']
                        tasks = TaskTable.getTaskByChatUserId(chatId)

                        if(len(tasks) == 0):
                            continue

                        morphAnalyzer = MorphAnalyzer()

                        decl1 = morphAnalyzer.parse(
                            'новая')[0].make_agree_with_number(len(tasks)).word

                        decl2 = morphAnalyzer.parse(
                            'заявка')[0].make_agree_with_number(len(tasks)).word

                        headingMessageId = bot.send_message(
                            chatId, f"У вас есть {decl1} {decl2}").message_id

                        for task in tasks:
                            bot.send_chat_action(chatId, 'typing')

                            buttons = (
                                InlineKeyboardButton(
                                    'Принять', callback_data='tasks:|{"id":%s,"status":1, "orgId":%s, "msgId":%s}' % (task.id, task.operatorOrgId, headingMessageId)),
                                # InlineKeyboardButton(
                                #     "Отработать", callback_data='tasks:|{"id":%s,"status":2, "orgId":%s, "msgId":%s}' % (task.id, task.operatorOrgId, headingMessageId))
                            )

                            markup = BaseController.generateInlineButtons(
                                buttons)

                            bot.send_message(chatId, BaseController.getTaskStringTemplate(
                                task), parse_mode="html", reply_markup=markup)

                            # Интервал перед отправкой сообщений
                            time.sleep(1)

                        # Интервал перед итерированиями пользователей
                        time.sleep(5)

                    # Интервал перед запросами базы данных
                    time.sleep(interval)

                except Exception as error:
                    appLog.error(f"{tasksDbThread.name} was terminated")
                    appLog.exception(error)

                    return None

        tasksDbThread = Thread(target=tasksDbWorker)
        tasksDbThread.name = "TasksDbThread"
        tasksDbThread.start()

        # Запуск потока на проверку активности потока TasksDbThread
        def tasksDbThreadAliveChecker() -> None:
            while True:
                if not tasksDbThread.is_alive():
                    tasksDbThread.join()
                    appLog.info(f"{tasksDbThread.name} was restarted")

                time.sleep(60)

        Thread(target=tasksDbThreadAliveChecker).start()
