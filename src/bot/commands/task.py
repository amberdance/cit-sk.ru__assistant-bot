import re
import ast
import os
import time
from datetime import datetime
from threading import Thread
from pymorphy2 import MorphAnalyzer
from telebot.apihelper import ApiTelegramException
from telebot.types import CallbackQuery
from config import BASE_DIR
from controllers.base import BaseController, TeleBot, Message, InlineKeyboardButton, appLog
from db.storage.chat import ChatUserStorage, ChatUserModel, MessageStorage
from db.storage.assistant import TaskStorage, TaskModel


class TaskHandler:
    def initialize(bot: TeleBot):

        @bot.message_handler(func=lambda message: re.findall(r"tasks", message.text))
        def getTasksCommand(message: Message, tasksLimit: int = 30) -> None:

            if BaseController.isPublicChat(message):
                return

            chatId = message.chat.id

            if(not ChatUserStorage.isUserRegistered(message.from_user.id)):
                return bot.send_message(chatId, "Сперва выполните регистрацию /reg")

            messageParams = message.text.split("-")
            statusId = 0

            if(len(messageParams) > 1 and messageParams[1]):
                statusId = messageParams[1].strip()

            try:
                user = ChatUserStorage.getFields(ChatUserModel.astUserId, ChatUserModel.role, filter=[
                    ChatUserModel.chatUserId == chatId])[0]
                isAdmin = bool(user['role'] == 1)
                tasks = TaskStorage.getByOperatorId(
                    user['astUserId'], statusId, isOperatorAdmin=isAdmin)
                tasksLen = len(tasks)

                if(tasksLen == 0):
                    return bot.send_message(chatId, "Заявки не найдены")

                if(tasksLen > tasksLimit):
                    return bot.send_message(chatId, "Найдено слишком много заявок, воспользуйтесь desktop или web версией программы")

                for task in tasks:
                    btns = []

                    if task.status == 0 and not isAdmin:
                        btns.append(InlineKeyboardButton(
                            "Принять", callback_data='tasks:|{"id":%s,"status":1}' % (task.id)))

                    elif task.status == 1 and not isAdmin:
                        btns.append(InlineKeyboardButton(
                            "Отработать", callback_data='tasks:|{"id":%s,"status":2}' % (task.id)))

                    bot.send_message(chatId, BaseController.getTaskStringTemplate(
                        task), parse_mode="html", reply_markup=None if len(btns) == 0 else BaseController.generateInlineButtons(btns))

            except ApiTelegramException as error:
                appLog.exception(error)
                bot.send_message(chatId, 'Что-то пошло не так')

            except Exception as error:
                appLog.exception(error)

        # update task callback handler
        @bot.callback_query_handler(func=lambda message: message.data.split("|")[0].find("tasks:") == 0)
        def updateTaskCommand(msg: CallbackQuery) -> None:
            payload = ast.literal_eval(msg.data.split("|")[1])
            chatId = msg.message.chat.id
            messageId = msg.message.id

            try:
                task = TaskStorage.getModel(TaskModel.id == payload['id'])

                # preventing unnecessary update
                if task.status == 1 and payload['status'] == 1:
                    return bot.delete_message(chatId, messageId)

                task.status = payload['status']
                task.operatorId = ChatUserStorage.getFields(ChatUserModel.astUserId, filter=[
                                                            ChatUserModel.chatId == chatId])[0]['astUserId']

                if(task.status == 2):
                    messageFile = BASE_DIR + f"/bot/messages/{chatId}.py"
                    data = []

                    if os.path.isfile(messageFile):
                        file = open(messageFile, "r")
                        data = file.read().split("\n")

                    if str(task.id) in data:
                        return

                    bot.send_message(
                        chatId, f"Напишите комментарий к заявке <b>{task.id}</b>", parse_mode="html")
                    # bot.delete_message(chatId, messageId)

                    with open(messageFile, "a+") as file:
                        file.write(str(task.id) + "\n")

                    # bot.edit_message_reply_markup(
                    #     chatId, messageId, reply_markup=None)

                    return bot.register_next_step_handler(
                        msg.message, updateServiceDescriptionStep, task)

                task.serviceStartData = datetime.now().isoformat(" ", "seconds")

                TaskStorage.updateModel()

                bot.delete_message(chatId, messageId)
                bot.send_message(
                    chatId, f"Заявка <b>{task.id}</b> принята в работу", parse_mode="html")

            except ApiTelegramException as error:
                appLog.exception(error)
                bot.send_message(chatId, "Что-то пошло не так")

            except Exception as error:
                appLog.exception(error)

        def updateServiceDescriptionStep(message: Message, task: TaskModel) -> None:
            if message.text == "/cancel":
                bot.clear_step_handler_by_chat_id(message.chat.id)
                bot.send_message(message.chat.id, "Действие отменено")

                return

            try:
                if message.text is None:
                    bot.send_message(
                        message.chat.id, "Поле комментарий не заполнено")

                    return bot.register_next_step_handler(message, updateServiceDescriptionStep, task)

                elif len(message.text) < 10:
                    bot.send_message(
                        message.chat.id, "Комментарий слишком короткий")

                    return bot.register_next_step_handler(message, updateServiceDescriptionStep, task)

                task.serviceDescr = message.text
                task.serviceEndData = datetime.now().isoformat(" ", "seconds")

                TaskStorage.updateModel()

                bot.send_message(
                    message.chat.id, f"Заявка <b>{task.id}</b> отработана", parse_mode="html")

            except Exception as error:
                appLog.error(error)
                bot.send_message(message.chat.id, "Что-то пошло не так")

    @staticmethod
    def scanningTasks(bot: TeleBot, interval: int) -> None:
        def tasksDbWorker(interval=interval):
            while True:
                try:
                    users = ChatUserStorage.getFields(
                        ChatUserModel.id,
                        ChatUserModel.astUserId,
                        ChatUserModel.username,
                        ChatUserModel.chatId,
                        ChatUserModel.role,
                        filter=[ChatUserModel.isBlocked == False, ChatUserModel.isSubscriber == True])

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

                            bot.send_message(chatId, BaseController.getTaskStringTemplate(task), parse_mode="html", reply_markup=None if len(
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
