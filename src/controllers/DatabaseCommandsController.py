from io import SEEK_END
import time
import re
from telebot import types
from controllers.BaseControllers import BaseController, ThreadController, Message, TeleBot, CallbackQuery, appLog
from db.tables.chat import *
from db.tables.assistant import *


class DatabaseCommandsController(BaseController):

    @staticmethod
    def initializeMessageHandler(bot: TeleBot) -> None:

        ThreadController.startTaskDbThreading(bot)

        # To do: добавить отмену для регистрации
        @bot.message_handler(commands=["reg"])
        def registerCommandStepOne(message: Message):
            # сперва проверка на наличие пользователя в базе данных
            if(ChatUserTable.isUserRegistered(message.from_user.id)):
                username = ChatUserTable.getUserFields(
                    ChatUserModel.username, filter=[ChatUserModel.chatUserId == message.from_user.id])['username']

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

            # список организаций по соответствию email, указанным пользвателем
            orgList = AstUserTable.getOrganization(
                AstUserModel.email == email, AstOrgUserModel.status == 1)

            # вызываем данный шаг до тех пор, пока не будет найдено соответствие по email
            if(bool(orgList) is False):
                cancelBtn = types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton("отмена", callback_data="0"))

                bot.send_message(
                    message.chat.id, f'Пользователь с логином <b>{email}</b> не найден, попробуйте другой', reply_markup=cancelBtn, parse_mode="html")

                return bot.register_next_step_handler(message, registerCommandStepTwo)

            else:
                return registerCommandStepThree(message, orgList)

        def registerCommandStepThree(message: Message, orgList: list) -> None:
            # список названий организаций в виде строки с переносом
            orgLabels = "\n".join(set(i.title for i in orgList))
            username = orgList[0].username
            key = types.InlineKeyboardMarkup()
            args = f"1|{orgList[0].userId}|{orgList[0].orgId}"
            btn1 = types.InlineKeyboardButton(
                text="Да", callback_data=args)
            btn2 = types.InlineKeyboardButton(
                text="Нет", callback_data="0")

            key.add(btn1, btn2)

            bot.send_message(
                message.chat.id, f"<b>{username}, нашел список организаций за которыми вы закреплены:</b>\n{orgLabels}\n<b>Все верно</b> ?", reply_markup=key, parse_mode="html")

        @bot.message_handler(func=lambda message: re.findall(r"tasks", message.text) and message.chat.type == 'private')
        def getTasksCommand(message: Message) -> None:
            chatId = message.chat.id
            messageParams = message.text.split("-")
            statusId = 0

            if(len(messageParams) > 1):
                statusId = TaskTable.getStatusId(messageParams[1].strip())

            if(not ChatUserTable.isUserRegistered(chatId)):
                bot.send_message(chatId, "Сперва выполните регистрацию /reg")

            tasks = TaskTable.getTaskByChatUserId(chatId, statusId)

            if(bool(tasks) is False):
                return bot.send_message(chatId, "Заявок не найдено")

            for i, task in enumerate(tasks):
                bot.send_chat_action(chatId, 'typing')
                task['status'] = TaskTable.getStatusLabel(task['status'])
                bot.send_message(chatId, f"<b>Номер заявки:</b> {task['id']}" +
                                 f"\n<b>Статус:</b> {task['status']}" +
                                 f"\n<b>Организация:</b> {task['org']}" +
                                 f"\n<b>Дата создания:</b> {task['orderDate']}" +
                                 f"\n<b>Неисправность:</b> {task['descr']}", parse_mode="html")

                if(i > 10):
                    return bot.send_message(chatId, "Найдено слишком много заявок, используйте другие критерии поиска или как-нибудь в другой раз")

        @bot.callback_query_handler(func=lambda message: True)
        def registrationInlineHandler(msg: CallbackQuery):
            payload = msg.data.split("|")

            # обработка кнопки отмены
            if payload[0] == '0':
                bot.clear_step_handler(msg.message)
                bot.send_message(msg.message.chat.id,
                                 "Ладно, в другой раз")

            # обработка кнопки да (регистрация юзера)
            elif payload[0] == "1":
                bot.send_chat_action(msg.message.chat.id, 'typing')

                try:
                    user = AstUserTable.getAstUserModel(
                        AstUserModel.id == payload[1])

                    fields = {
                        "chatId": msg.message.chat.id,
                        "chatUserId": msg.from_user.id,
                        "astOrgId": payload[2],
                        "astUserId": user.id,
                        "username": user.username,
                        "email": user.email,
                        "role": 2
                    }

                    ChatUserTable.addUser(ChatUserModel(**fields))
                    bot.send_message(
                        msg.message.chat.id, f"{user.username}, регистрация прошла успешно!")

                except Exception:
                    bot.send_message(
                        msg.message.chat.id, "Что-то пошло не так")
                    appLog.exception(Exception)

            # удаление кнопок
            bot.edit_message_reply_markup(
                msg.message.chat.id, msg.message.id, reply_markup=None)
