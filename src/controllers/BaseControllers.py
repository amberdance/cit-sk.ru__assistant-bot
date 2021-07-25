from abc import ABC, abstractmethod
import logging
import time
from threading import Thread, Timer
from typing import Any, Union
from telebot import TeleBot
from telebot.types import CallbackQuery, Message
from db.tables.assistant import TaskTable, TaskModel


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
            while True:
                try:
                    bot.send_chat_action(686739701, 'typing')
                    task = TaskTable.getFreshTask(
                        TaskModel.clientOrgId == 135)[0]
                    bot.send_message(
                        686739701, f"Database polling with 5 min timeout.\nRandom task<b>№ {task.id}</b> от <b>{task.orderDate}</b>: \n<b>{task.descr}</b>", parse_mode="html")

                    time.sleep(interval)

                except Exception as error:
                    appLog.error(f"{tasksDbThread.name} was terminated")
                    appLog.exception(error)

                    return None

        tasksDbThread = Timer(10, tasksDbWorker)
        tasksDbThread.name = "TasksDbThread"
        tasksDbThread.start()

        appLog.info(f"{tasksDbThread.name} was started")

        # Запуск потока на проверку активности потока TasksDbThread
        def tasksDbThreadAliveChecker() -> None:
            while True:
                if not tasksDbThread.is_alive():
                    tasksDbThread.join()
                    appLog.info(f"{tasksDbThread.name} was restarted")

                time.sleep(60)

        Thread(target=tasksDbThreadAliveChecker).start()
