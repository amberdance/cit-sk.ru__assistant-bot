import re
from typing import Union, final
from telebot.apihelper import ApiTelegramException
from telebot.types import CallbackQuery, InlineKeyboardMarkup
from bot.controllers.base import BaseController, TeleBot, Message, InlineKeyboardButton, appLog
from db.models.chat import UserModel
from db.storage.assistant import TaskStorage
from db.storage.chat import UserStorage


@final
class TaskMenuHandler:

    bot: TeleBot = None
    menu: dict = None
    CALLBACK_ID: list = []

    def __init__(self, bot: TeleBot) -> None:
        self.bot = bot
        self.menu = {
            "root": {
                "title": "Выберите пункт меню",
                "btn": (
                    InlineKeyboardButton(
                        'Список заявок', callback_data="tm|tasksList"),
                    InlineKeyboardButton(
                        'Поиск заявки', callback_data="tm|filterById")
                )
            },

            "tasksList": {
                "title": "Поиск по статусу заявки",
                "btn": (
                    InlineKeyboardButton(
                        'Новая', callback_data="tm|filterByStatus|0"),
                    InlineKeyboardButton(
                        'В работе', callback_data="tm|filterByStatus|1"),
                    InlineKeyboardButton(
                        'Отработана', callback_data="tm|filterByStatus|2"),
                    InlineKeyboardButton(
                        'Отменена', callback_data="tm|filterByStatus|3"),
                    InlineKeyboardButton('« Назад', callback_data="tm|root"),
                ),
            },

            "filterById": {
                "title": "Поиск по номеру заявки",
                "callback": self.filterByTaskId,
                "btn": InlineKeyboardButton('« Назад', callback_data="tm|root"),
            },

            "filterByStatus": {
                "callback": self.filterTasksByStatus
            },
        }

        self.initialize()

    def initialize(self) -> None:
        @self.bot.message_handler(['tasks'])
        def startMenu(message: Message):

            if BaseController.isPublicChat(message):
                return

            if(not UserStorage.isUserRegistered(message.chat.id)):
                return self.bot.send_message(message.chat.id, "Сперва выполните регистрацию /reg")

            self.bot.send_message(
                message.chat.id, self.menu['root']['title'], reply_markup=BaseController.generateInlineButtons(self.menu['root']['btn']))

        @self.bot.callback_query_handler(lambda message: message.data.find("tm") == 0)
        def menuCallbackHandler(call: CallbackQuery) -> Union[callable, None]:
            try:
                payload = call.data.split("|")
                key = payload[1]
                args = payload[2] if len(payload) > 2 else None
                title = self.menu[key]['title'] if 'title' in self.menu[key] else None
                btn = self.menu[key]['btn'] if 'btn' in self.menu[key] else None
                callback = self.menu[key]['callback'] if 'callback' in self.menu[key] else None

                if title is not None:
                    self.bot.edit_message_text(
                        title, call.message.chat.id, call.message.id, call.inline_message_id, reply_markup=BaseController.generateInlineButtons(btn))

                if callback is not None:
                    return callback(call.message, call) if args is None else callback(call.message, call, args)

            except (KeyError, IndexError, ApiTelegramException):
                self.bot.send_message(
                    call.message.chat.id, "Что-то пошло не так")

            except Exception as error:
                appLog.exception(error)

    def filterByTaskId(self, message: Message, call: CallbackQuery) -> None:
        self.bot.send_message(message.chat.id, "Введите номер заявки")
        self.bot.register_next_step_handler(
            message, self.getTaskByIdStep, call)

    # Todo: Предотвратить рекурсию, которую можно вызвать из предыдущего в чате inline меню
    def getTaskByIdStep(self, message: Message, call: CallbackQuery) -> None:
        chatId = message.chat.id

        def repeatStep() -> None:
            self.bot.register_next_step_handler(
                message, self.getTaskByIdStep, call)

        if(message.text == "/cancel"):
            self.bot.send_message(chatId, "Поиск заявки по номеру отменен")

            return self.bot.clear_step_handler_by_chat_id(chatId)

        if(re.findall(r"\D", message.text)):
            self.bot.send_message(
                chatId, "Принимаются только числовые значения")

            return repeatStep()

        user = UserStorage.getFields(UserModel.astUserId, UserModel.role)[0]
        taskId = int(message.text)
        task = TaskStorage.getByConditions(
            operatorId=user['astUserId'], taskId=taskId, isUserAdmin=bool(user['role'] == 1))

        if bool(task) is False:
            self.bot.send_message(
                chatId, f"Заявка <b>{taskId}</b> не найдена", parse_mode="html")

            return repeatStep()

        else:
            self.bot.send_message(
                chatId, BaseController.generateTaskHTMLTemlpate(task), parse_mode="html")

        return repeatStep()

    def filterTasksByStatus(self, message: Message, call: CallbackQuery, status: int = 0) -> None:
        status = int(status)

        try:
            isAdmin = UserStorage.isAdmin(message.chat.id)
            tasks = list(reversed(TaskStorage.getByConditions(operatorId=UserStorage.getOperatorId(
                message.chat.id), statusId=status, limit=6 if status > 0 else None, order="desc", isUserAdmin=isAdmin)))
            tasksLen = len(tasks)

            if(tasksLen == 0):
                return self.bot.answer_callback_query(call.id, "Заявки не найдены")

            lastTask = tasks[tasksLen - 1]
            lastTaskMessageId = 0

            for i, task in enumerate(tasks):
                btns = BaseController.generateUpdateStatusButtons(
                    task.id, message.chat.id, status)

                lastTaskMessageId = self.bot.send_message(message.chat.id, BaseController.generateTaskHTMLTemlpate(task), parse_mode="html",
                                                          reply_markup=None if len(btns) == 0 else BaseController.generateInlineButtons(btns)).message_id

                if i == (tasksLen - 1):
                    break

            markup = InlineKeyboardMarkup()
            markup.add(*BaseController.generateUpdateStatusButtons(
                lastTask.id, message.chat.id, status))
            markup.add(*self.menu['tasksList']['btn'])

            self.bot.edit_message_text(BaseController.generateTaskHTMLTemlpate(
                lastTask), message.chat.id, lastTaskMessageId, parse_mode="html", reply_markup=markup)

            self.bot.delete_message(message.chat.id, message.id)

        except Exception as error:
            self.bot.send_message(message.chat.id, "Что-то пошло не так")
            appLog.exception(error)
