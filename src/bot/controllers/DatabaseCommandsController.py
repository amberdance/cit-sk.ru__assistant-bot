import time
import re
from db.tables.ChatUserTable import ChatUserTable, ChatUserModel
from db.tables.TaskTable import TaskTable, TaskModel
from .BaseController import BaseController, TeleBot, Message
from config import IS_DEBUG_MODE


class DatabaseCommandsController(BaseController):

    @staticmethod
    def initializeMessageHandler(bot: TeleBot) -> None:
        @bot.message_handler(commands=['register', 'reg'])
        def registerUserCommand(message: Message):

            try:
                if(ChatUserTable.isUserRegistered(message.from_user.id)):
                    # to do: распознать пол
                    BaseController.sendMessage(
                        bot, message, f"{message.from_user.first_name} {message.from_user.last_name}, ранее Вы уже были зарегистрированы. Чтобы узнать Ваш id введите /userid")
                else:
                    fields = {
                        "astUserId": 1,
                        "chatId": message.chat.id,
                        "chatUserId": message.from_user.id
                    }

                    ChatUserTable.addUser(ChatUserModel(**fields))

                    BaseController.sendMessage(
                        bot, message, "Регистрация прошла успешно! Чтобы узнать свой id напишите команду /userid")
            except Exception as error:
                errorMsg = "К сожалению, не удалось вас зарегистрировать, попробуйте еще раз" if IS_DEBUG_MODE is False else error
                BaseController.sendMessage(bot, message, errorMsg)

        @bot.message_handler(regexp="task")
        def getTaskCommand(message: Message):
            bot.send_chat_action(message.chat.id, 'typing')

            taskId = re.findall("\d.*", message.text)

            if bool(taskId) is False:
                return BaseController.sendMessage(
                    bot, message, "Укажите команду с номером заявки, например: /task666")

            task = TaskTable.getTaskModel(TaskModel.id == taskId[0])

            if hasattr(task, "id"):
                BaseController.sendMessage(
                    bot, message, f"<b>Номер заявки:</b> {task.id}," +
                    f"\n<b>Дата создания:</b> {task.orderDate}," +
                    f"\n<b>Неисправность:</b> {task.descr}", parseMode="html")
            else:
                BaseController.sendMessage(
                    bot, message, f"Заявка под номером {taskId[0]} не найдена")
