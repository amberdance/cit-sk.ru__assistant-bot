
import ast
import re
from sqlalchemy.exc import IntegrityError
from controllers.BaseControllers import *
from db.tables.chat import *
from db.tables.assistant import *


class DatabaseCommandsController(BaseController):

    @staticmethod
    def initializeMessageHandler(bot: TeleBot) -> None:

        ThreadController.startTaskDbThreading(bot)

        # Todo: добавить отмену для регистрации
        @bot.message_handler(commands=["reg"])
        def registerCommandStepOne(message: Message):

            # сперва проверка на наличие пользователя в базе данных
            if(ChatUserTable.isUserRegistered(message.from_user.id)):
                username = ChatUserTable.getUserFields(
                    ChatUserModel.username, filter=[ChatUserModel.chatUserId == message.from_user.id])[0]['username']

                return BaseController.sendMessage(
                    bot, message, f"{username}, ранее Вы уже были зарегистрированы. Чтобы узнать Ваш Id введите /userid")

            if(message.chat.type != "private"):
                bot.reply_to(
                    message, f"{message.from_user.full_name}, для регистрации напишите мне в ЛС /reg")

                return bot.register_next_step_handler(message, registerCommandStepTwo)

            BaseController.sendMessage(
                bot, message, "Введите логин вашей учетной записи в ассистенте")

            bot.register_next_step_handler(message, registerCommandStepTwo)

        def registerCommandStepTwo(message: Message) -> None:
            email = message.text

            if(bool(re.findall(r'[\w\.-]+@[\w\.-]+(?:\.[\w]+)+', email)) is False):
                bot.send_message(message.chat.id, 'Введите корректный email')
                return bot.register_next_step_handler(message, registerCommandStepTwo)

            # список организаций в соответствии с email, указанным пользвателем
            orgList = AstUserTable.getOrganization(
                AstUserModel.email == email, AstOrgUserModel.status == 1)

            # вызываем данный шаг до тех пор, пока не будет найдено соответствие по email
            if(bool(orgList) is False):
                cancelBtn = BaseController.generateInlineButtons(
                    (InlineKeyboardButton("отмена", callback_data="reg:0"),))

                bot.send_message(
                    message.chat.id, f'Пользователь с логином <b>{email}</b> не найден, попробуйте другой', reply_markup=cancelBtn, parse_mode="html")

                return bot.register_next_step_handler(message, registerCommandStepTwo)

            else:
                return registerCommandStepThree(message, orgList)

        def registerCommandStepThree(message: Message, orgList: list) -> None:
            # список названий организаций в виде строки с переносом
            orgLabels = "\n".join(set(i.title for i in orgList))
            username = orgList[0].username
            args = f"reg:1|{orgList[0].userId}|{orgList[0].orgId}"
            buttons = (InlineKeyboardButton(
                text="Да", callback_data=args), InlineKeyboardButton("Нет", callback_data="reg:0"))
            markup = BaseController.generateInlineButtons(buttons)

            bot.send_message(
                message.chat.id, f"<b>{username}, нашел список организаций за которыми вы закреплены:</b>\n{orgLabels}\n<b>Все верно</b> ?", reply_markup=markup, parse_mode="html")

        @bot.message_handler(func=lambda message: re.findall(r"tasks", message.text) and message.chat.type == 'private')
        def getTasksCommand(message: Message) -> None:
            chatId = message.chat.id
            messageParams = message.text.split("-")
            statusId = 0

            if(len(messageParams) > 1):
                statusId = TaskTable.getStatusId(messageParams[1].strip())

            if(not ChatUserTable.isUserRegistered(chatId)):
                return bot.send_message(chatId, "Сперва выполните регистрацию /reg")

            try:
                tasks = TaskTable.getTaskByChatUserId(chatId, statusId)

                if(bool(tasks) is False):
                    return bot.send_message(chatId, "Заявки не найдены")

                for i, task in enumerate(tasks):
                    bot.send_chat_action(chatId, 'typing')
                    bot.send_message(chatId, BaseController.getTaskStringTemplate(
                        task), parse_mode="html")

                    if(i > 10):
                        return bot.send_message(chatId, "Найдено слишком много заявок, используйте другие критерии поиска или как-нибудь в другой раз")

            except Exception as error:
                appLog.exception(error)
                bot.send_message(chatId, 'Что-то пошло не так')

        # Обработчик команды /reg
        @bot.callback_query_handler(func=lambda message: message.data.split("|")[0].find("reg:") == 0)
        def registrationInlineHandler(msg: CallbackQuery):
            payload = msg.data.split("|")
            chatId = msg.message.chat.id

            # обработка кнопки отмены
            if payload[0] == 'reg:0':
                bot.clear_step_handler(msg.message)
                bot.send_message(chatId, "Ладно, в другой раз")

            # обработка кнопки да (регистрация юзера)
            elif payload[0] == "reg:1":
                bot.send_chat_action(chatId, 'typing')

                try:
                    user = AstUserTable.getAstUserModel(
                        AstUserModel.id == payload[1])

                    fields = {
                        "chatId": chatId,
                        "chatUserId": msg.from_user.id,
                        "astOrgId": payload[2],
                        "astUserId": user.id,
                        "username": user.username,
                        "email": user.email,
                        "role": 1
                    }

                except Exception as error:
                    bot.send_message(chatId, "Что-то пошло не так")
                    appLog.exception(error)

                try:
                    ChatUserTable.addUser(ChatUserModel(**fields))
                    bot.send_message(
                        chatId, f"{user.username}, регистрация прошла успешно!")

                except IntegrityError as error:
                    bot.send_message(
                        chatId, 'Пользователь с таким email уже зарегистрирован')

            bot.edit_message_reply_markup(
                chatId, msg.message.id, reply_markup=None)

            bot.delete_message(chatId, msg.message.id)

        # Обработчик принятия, отработки заявки при получении заявок от рассылки бота
        @bot.callback_query_handler(func=lambda message: message.data.split("|")[0].find("tasks:") == 0)
        def updateTaskCommand(msg: CallbackQuery) -> None:

            if not ChatUserTable.isUserRegistered(msg.from_user.id):
                return

            payload = ast.literal_eval(msg.data.split("|")[1])
            chatId = msg.message.chat.id

            try:
                task = TaskTable.getTaskModel(TaskModel.id == payload['id'])
                task.status = payload['status']

                if task.status == 1:
                    task.serviceStartData = datetime.now().isoformat(" ", "seconds")
                else:
                    task.serviceEndData = datetime.now().isoformat(" ", "seconds")

                TaskTable.upadteTask()

                # Если новых заявок больше не осталось, то удаляется вступительное сообщение о наличии новых заявок
                if len(TaskTable.getTaskFields(TaskModel.id, filter=[TaskModel.status == 0, TaskModel.operatorOrgId == payload['orgId']])) == 0:
                    bot.delete_message(chatId, payload['msgId'])

                # successWord = 'принята' if payload['status'] == 1 else 'отработана'

                bot.edit_message_reply_markup(
                    chatId, msg.message.id, reply_markup=None)

                bot.reply_to(msg.message, f"Заявка {task.id} принята в работу")

            except Exception as error:
                appLog.exception(error)
