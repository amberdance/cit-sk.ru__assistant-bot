import re
from db.models.chat import UserModel
from db.tables.chat import UserTable
from db.tables.assistant import TaskTable, TaskModel, AstUserTable, AstUserModel
from .BaseController import BaseController, TeleBot, Message, CallbackQuery, types


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

            bot.send_chat_action(message.chat.id, 'typing')

            email = message.text
            # список организаций по соответствию email, указанным пользвателем
            orgList = AstUserTable.getOrganization(AstUserModel.email == email)

            # вызываем данный шаг до тех пор, пока не будет найдено соответствие по email
            if(bool(orgList) is False):
                cancelBtn = types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton("отмена", callback_data="cancel"))

                bot.send_message(
                    message.chat.id, f'Пользователь с логином <b>{email}</b> на найден, попробуйте другой', reply_markup=cancelBtn, parse_mode="html")

                return bot.register_next_step_handler(message, registerCommandStepTwo)

            else:
                bot.register_next_step_handler(
                    message, registerCommandStepThree(message, orgList))

        def registerCommandStepThree(message: Message, orgList: list) -> None:

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

            if payload[0] == 'cancel':
                bot.clear_step_handler(msg.message)
                bot.send_message(msg.message.chat.id,
                                 "Принято, в другой раз у тебя всн получится")

            elif payload[0] == "1":
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
                except Exception as error:
                    bot.send_message(
                        msg.message.chat.id, "Что-то пошло не так, попробуйте еще раз, но сомневаюсь, что это поможет")
                    print(error)

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
