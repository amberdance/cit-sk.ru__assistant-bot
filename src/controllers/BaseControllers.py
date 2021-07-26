from abc import ABC, abstractmethod
import logging
import time
from threading import Thread, Timer
from typing import Any, Union
from telebot import TeleBot
from telebot.types import CallbackQuery, Message
from db.tables.assistant import TaskTable
from db.tables.chat import ChatUserTable, ChatUserModel


appLog: logging.Logger = logging.getLogger("Application")


class BaseController(ABC):

    @abstractmethod
    def initializeMessageHandler(bot: TeleBot) -> None:
        ...

    def sendMessage(bot: TeleBot, message: Union[Message, CallbackQuery],  text: Any, parseMode: str = None):
        """Отправляет сообщение в лс, если боту пишут в группе, и в общий чат, если пишут в лс"""
        bot.send_message(message.chat.id, text, parse_mode=parseMode) if(
            message.chat.type == 'private') else bot.send_message(message.from_user.id, text, parse_mode=parseMode)


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
                        ChatUserModel.username, ChatUserModel.chatUserId, filter=[ChatUserModel.isBlocked == False])

                    for user in subscribers:
                        chatId = user['chatUserId']
                        tasks = TaskTable.getTaskByChatUserId(chatId)

                        if(len(tasks) == 0):
                            continue

                        for task in tasks:
                            bot.send_chat_action(chatId, 'typing')
                            bot.send_message(chatId, f"{user['username']} У вас есть новые заявки:\n" +
                                             f"<b>Номер заявки:</b> {task['id']}" +
                                             f"\n<b>Дата создания:</b> {task['orderDate']}" +
                                             f"\n<b>Статус:</b> {TaskTable.getStatusLabel(task['status'])}" +
                                             f"\n<b>Организация:</b> {task['org']}" +
                                             f"\n<b>Неисправность:</b> {task['descr']}", parse_mode="html")

                            # Интервал перед отправкой сообщений
                            time.sleep(2)

                        # Интервал перед итерированиями пользователей
                        time.sleep(5)

                    # Интервал перед запросами базы данных
                    time.sleep(interval)

                except Exception as error:
                    appLog.error(f"{tasksDbThread.name} was terminated")
                    appLog.exception(error)

        tasksDbThread = Timer(10, tasksDbWorker)
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
