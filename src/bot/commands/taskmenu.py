from typing import Union
from telebot.apihelper import ApiTelegramException
from telebot.types import CallbackQuery, InlineKeyboardMarkup
from controllers.base import BaseController, TeleBot, Message, InlineKeyboardButton, appLog
from db.storage.assistant import TaskStorage
from db.storage.chat import ChatUserStorage


class TaskMenuHandler:

    __bot: TeleBot = None
    __menu = None

    def __init__(self, bot: TeleBot) -> None:
        self.__bot = bot
        self.__menu = {
            "root": {
                "title": "Меню заявок",
                "btn": InlineKeyboardButton('Список заявок', callback_data="tm|tasksList"),
            },

            "tasksList": {
                "title": "Выберите статус заявки",
                "btn": (
                    InlineKeyboardButton(
                        'Новая', callback_data="tm|filterByStatus|0"),
                    InlineKeyboardButton(
                        'В работе', callback_data="tm|filterByStatus|1"),
                    InlineKeyboardButton(
                        'Отработана', callback_data="tm|filterByStatus|2"),
                    InlineKeyboardButton(
                        'Отменена', callback_data="tm|filterByStatus|3"),
                ),
            },

            "filterByStatus": {
                "callback": self.__filterTasksByStatus
            },

            # "backToRoot": {
            #     "btn": InlineKeyboardButton('« Назад', callback_data="tm|root"),
            # },
        }

        self.__initialize()

    def __initialize(self) -> None:
        @self.__bot.message_handler(['tasks'])
        def startMenu(message: Message):

            if BaseController.isPublicChat(message):
                return

            if(not ChatUserStorage.isUserRegistered(message.chat.id)):
                return self.__bot.send_message(message.chat.id, "Сперва выполните регистрацию /reg")

            self.__bot.send_message(
                message.chat.id, self.__menu['tasksList']['title'], reply_markup=BaseController.generateInlineButtons(self.__menu['tasksList']['btn']))

        @self.__bot.callback_query_handler(lambda message: message.data.find("tm") == 0)
        def menuCallbackHandler(call: CallbackQuery) -> Union[callable, None]:
            try:
                payload = call.data.split("|")
                key = payload[1]
                args = payload[2] if len(payload) > 2 else None
                callback = self.__menu[key]['callback'] if 'callback' in self.__menu[key] else None

                if callback is not None:
                    return callback(call.message, call, args)

            except (KeyError, IndexError, ApiTelegramException) as error:
                self.__bot.send_message(
                    call.message.chat.id, "Что-то пошло не так")
                appLog.exception(error)

    def __filterTasksByStatus(self, message: Message, call: CallbackQuery, status: str = 0) -> None:
        status = int(status)

        try:
            tasks = list(reversed(TaskStorage.getByOperatorId(ChatUserStorage.getOperatorId(
                message.chat.id), status, limit=6 if status > 0 else None, order="desc")))
            tasksLen = len(tasks)

            if(tasksLen == 0):
                return self.__bot.answer_callback_query(call.id, "Заявки не найдены")

            lastTask = tasks[tasksLen - 1]
            lastTaskMessageId = 0

            for i, task in enumerate(tasks):
                btns = BaseController.generateUpdateStatusButtons(
                    task.id, message.chat.id, status)

                lastTaskMessageId = self.__bot.send_message(message.chat.id, BaseController.getTaskHTMLTemlpate(task), parse_mode="html",
                                                            reply_markup=None if len(btns) == 0 else BaseController.generateInlineButtons(btns)).message_id

                if i == (tasksLen - 1):
                    break

            markup = InlineKeyboardMarkup()
            markup.add(*BaseController.generateUpdateStatusButtons(
                lastTask.id, message.chat.id, status))
            markup.add(*self.__menu['tasksList']['btn'])

            self.__bot.edit_message_text(BaseController.getTaskHTMLTemlpate(
                lastTask), message.chat.id, lastTaskMessageId, parse_mode="html", reply_markup=markup)

            self.__bot.delete_message(message.chat.id, message.id)

        except ApiTelegramException as error:
            appLog.exception(error)
            self.__bot.send_message(message.chat.id, "Что-то пошло не так")
