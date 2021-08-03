import ast
import os
import time
from datetime import datetime
from threading import Thread
from pymorphy2 import MorphAnalyzer
from telebot.apihelper import ApiTelegramException
from telebot.types import CallbackQuery
from config import BASE_DIR
from bot.controllers.base import BaseController, TeleBot, Message, InlineKeyboardButton, appLog
from db.storage.chat import ChatUserStorage, ChatUserModel
from db.storage.assistant import TaskStorage, TaskModel


class TaskHandler:

    @staticmethod
    def initialize(bot: TeleBot) -> None:

        # update task callback handler
        @bot.callback_query_handler(func=lambda message: message.data.split("|")[0].find("tasks:") == 0)
        def updateTaskCommand(call: CallbackQuery) -> None:
            payload = ast.literal_eval(call.data.split("|")[1])
            chatId = call.message.chat.id
            messageId = call.message.id

            try:
                task = TaskStorage.getModel(TaskModel.id == payload['id'])

                # preventing unnecessary update
                if task.status == payload['status']:
                    return bot.delete_message(chatId, messageId)

                task.status = payload['status']
                task.operatorId = ChatUserStorage.getOperatorId(chatId)

                if(task.status == 2):
                    # at first we should to prevent multiple closing tasks
                    msgDir = BASE_DIR + "/bot/messages/"
                    msgFile = msgDir + str(chatId) + ".txt"

                    if os.path.isfile(msgFile):
                        return

                    if not os.path.isdir(msgDir):
                        os.mkdir(msgDir)

                    with open(msgFile, "a+") as file:
                        data = '{"id":%s, "messageId":%s}' % (
                            str(chatId), str(messageId))

                        file.write(data + "\n")

                    bot.send_message(
                        chatId, f"Напишите комментарий к заявке <b>{task.id}</b>", parse_mode="html")

                    return bot.register_next_step_handler(
                        call.message, updateServiceDescriptionStep, task, messageId, msgFile)

                task.serviceStartData = datetime.now().isoformat(" ", "seconds")

                TaskStorage.updateModel()

                bot.answer_callback_query(
                    call.id,  f"Заявка {str(task.id)} принята в работу")
                bot.delete_message(chatId, messageId)

            except Exception as error:
                bot.send_message(chatId, "Что-то пошло не так")
                appLog.exception(error)

        def updateServiceDescriptionStep(message: Message, task: TaskModel,  taskMessageId: int, msgFile: str) -> None:
            chatId = message.chat.id

            if message.text == "/cancel":
                os.remove(msgFile)

                bot.clear_step_handler_by_chat_id(message.chat.id)
                bot.send_message(message.chat.id, "Действие отменено")

                return

            bot.send_chat_action(chatId, 'typing')

            if message.text is None:
                bot.send_message(chatId, "Поле комментарий не заполнено")

                return bot.register_next_step_handler(message, updateServiceDescriptionStep, task, taskMessageId, msgFile)

            elif len(message.text) < 6:
                bot.send_message(chatId, "Комментарий слишком короткий")

                return bot.register_next_step_handler(message, updateServiceDescriptionStep, task, taskMessageId, msgFile)

            task.serviceDescr = message.text
            task.serviceEndData = datetime.now().isoformat(" ", "seconds")

            try:
                TaskStorage.updateModel()
                os.remove(msgFile)

                bot.delete_message(chatId, taskMessageId)
                bot.send_message(
                    chatId, f"✅ Заявка <b>{task.id}</b> отработана", parse_mode="html")

            except Exception as error:
                bot.send_message(chatId, "Что-то пошло не так")
                appLog.exception(error)

    @staticmethod
    def scanningTasks(bot: TeleBot, interval: int) -> None:
        def tasksDbWorker(interval=interval):
            while True:
                try:
                    users = ChatUserStorage.getUsers()

                    if(bool(users) is False):
                        continue

                    for user in users:
                        isAdmin = bool(user['role'] == 1)
                        operatorId = user['astUserId']
                        chatId = user['chatId']
                        tasks = TaskStorage.getByOperatorId(
                            operatorId, isOperatorAdmin=isAdmin)

                        if(bool(tasks) is False):
                            continue

                        tasksLength = len(tasks)
                        decl = TaskHandler.__getDeclination(tasksLength)

                        bot.send_message(
                            chatId, f"У вас есть {tasksLength} {decl['status']} {decl['task']}")

                        if(len(tasks) > 10):
                            continue

                        appLog.info(
                            f"{tasksDbThread} sending tasks to user: {user['username']}, operator id: {operatorId}")

                        for task in tasks:
                            buttons = []

                            if not isAdmin:
                                buttons.append(InlineKeyboardButton('Принять', callback_data='tasks:|{"id":%s,"status":1}' % (
                                    task.id)))

                            bot.send_message(chatId, BaseController.getTaskHTMLTemlpate(task), parse_mode="html", reply_markup=None if len(
                                buttons) == 0 else BaseController.generateInlineButtons(buttons))

                        # delay imitation
                        time.sleep(len(tasks) + 2)

                    # scanning interval
                    time.sleep(interval)

                except ApiTelegramException as error:
                    # blocking user to prevent mailing if chat id is missing
                    if(str(error).find("message not found") != -1):

                        ChatUserStorage.updateByFields(
                            [ChatUserModel.astUserId == operatorId], {"isBlocked": True, "isSubscriber": False})

                except Exception as error:
                    appLog.exception(error)

        tasksDbThread = Thread(target=tasksDbWorker)
        tasksDbThread.name = "TasksDbThread"
        tasksDbThread.start()

    @staticmethod
    def __getDeclination(tasksLength: int):
        morphAnalyzer = MorphAnalyzer()

        return{
            "status": morphAnalyzer.parse('новая')[0].make_agree_with_number(tasksLength).word,
            "task": morphAnalyzer.parse('заявка')[0].make_agree_with_number(tasksLength).word
        }
