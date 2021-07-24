import re
from db.models.chat import UserModel
from db.tables.chat import UserTable
from db.tables.assistant import TaskTable, TaskModel, AstUserTable, AstUserModel
from .BaseController import BaseController, TeleBot, Message, CallbackQuery, types


MESSAGE_ID = 0
CHAT_ID = 0


class DatabaseCommandsController(BaseController):

    @staticmethod
    def initializeMessageHandler(bot: TeleBot) -> None:

        @bot.message_handler(commands=["registration", "reg"])
        def registerCommandStepOne(message: Message):

            # сперва проверка на наличие пользователя в базе данных
            if(UserTable.isUserRegistered(message.from_user.id)):
                username = UserTable.getUserFields(
                    UserModel.username, filter=[UserModel.chatUserId == message.from_user.id])[0]['username']

                return BaseController.sendMessage(
                    bot, message, f"{username}, ранее Вы уже были зарегистрированы. Чтобы узнать Ваш id введите /userid")

            if(message.chat.type != "private"):
                return bot.reply_to(message, "Команды подобного рода пишутся в лс")

            BaseController.sendMessage(
                bot, message, "Введите логин вашей учетной записи в ассистенте")

            bot.register_next_step_handler(message, registerCommandStepTwo)

        def registerCommandStepTwo(message: Message) -> None:
            global MESSAGE_ID
            global CHAT_ID

            MESSAGE_ID = message.id
            CHAT_ID = message.chat.id

            bot.send_chat_action(message.chat.id, 'typing')

            email = message.text

            # список организаций по соответствию email, указанным пользвателем
            orgList = AstUserTable.getOrganization(AstUserModel.email == email)

            if(bool(orgList) is False):
                return BaseController.sendMessage(
                    bot, message, f'Пользователь с логином <b>{email}</b> на найден', parseMode="html")

             # список названий организаций в виде строки с переносом
            orgLabels = "\n".join(set(i.title for i in orgList))
            key = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(
                text="Да", callback_data=str(f"1|{orgList[0].id}|{orgList[0].username}"))
            btn2 = types.InlineKeyboardButton(
                text="Нет", callback_data="0")

            key.add(btn1, btn2)

            bot.send_message(
                message.chat.id, f"<b>Список организаций, в которых вы состоите:</b>\n{orgLabels}\n<b>Все верно</b> ?", reply_markup=key, parse_mode="html")

        @bot.callback_query_handler(func=lambda message: True)
        def registrationInlineHandler(msg: CallbackQuery):
            payload = msg.data.split("|")

            if payload[0] == "1":
                try:
                    fields = {
                        "chatId": msg.message.chat.id,
                        "chatUserId": msg.from_user.id,
                        "astUserId": payload[1],
                        "username": payload[2]
                    }

                    UserTable.addUser(UserModel(**fields))
                    bot.send_message(
                        msg.message.chat.id, f"{payload[2]}, регистрация прошла успешно!")
                except Exception:
                    bot.send_message(
                        msg.message.chat.id, "Что-то пошло не так, попробуйте еще раз, но сомневаюсь, что это поможет")

            elif payload[0] == "0":
                bot.send_message(msg.message.chat.id,
                                 'Ладно. может быть, в другой раз')

            # удаление кнопок
            bot.edit_message_reply_markup(
                msg.message.chat.id, msg.message.id, reply_markup=None)

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
