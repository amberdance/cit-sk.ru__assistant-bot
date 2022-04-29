import logging
import re
from sqlalchemy.exc import IntegrityError
from telebot.types import CallbackQuery
from bot.controllers.base import BaseController, TeleBot, Message, InlineKeyboardButton, appLog
from db.storage.chat import UserStorage, UserModel
from db.storage.assistant import AstUserStorage, AstUserModel, AstOrgUserModel


class ChatUserHandler:

    @staticmethod
    def initialize(bot: TeleBot) -> None:
        @bot.message_handler(["reg"])
        def stepOne(message: Message):

            if BaseController.isPublicChat(message):
                return

            chatId = message.chat.id

            if(UserStorage.isUserRegistered(message.from_user.id)):
                username = UserStorage.getFields(
                    UserModel.username, filter=[UserModel.chatUserId == message.from_user.id])[0]['username']

                return bot.send_message(chatId, f"{username}, Вы уже зарегистрированы")

            message = bot.send_message(
                chatId, "Введите логин вашей учетной записи в ассистенте")

            bot.register_next_step_handler(message, stepTwo)

        def stepTwo(message: Message) -> None:
            email = message.text

            if(message.text == "/cancel"):
                bot.send_message(message.chat.id, "Регистрация отменена")

                return bot.clear_step_handler_by_chat_id(message.chat.id)

            if(bool(re.findall(r'[\w\.-]+@[\w\.-]+(?:\.[\w]+)+', email)) is False):
                bot.send_message(message.chat.id, 'Введите корректный email')

                return bot.register_next_step_handler(message, stepTwo)

            organizationList = AstUserStorage.getOrganization(
                AstUserModel.email == email.lower(), AstOrgUserModel.status == 1)

            if(bool(organizationList) is False):
                bot.send_message(
                    message.chat.id, f'Пользователь с логином <b>{email}</b> не найден.', parse_mode="html")

                return bot.register_next_step_handler(message, stepTwo)

            else:
                return stepThree(message, organizationList)

        def stepThree(message: Message, organizationList: list) -> None:

            orgLabelsStroke = "\n".join(
                set(f"-{org.title}" for org in organizationList))
            username = organizationList[0].username
            args = f"reg:1|{organizationList[0].userId}|{organizationList[0].orgId}"
            buttons = (InlineKeyboardButton(
                text="Да", callback_data=args), InlineKeyboardButton("Нет", callback_data="reg:0"))
            markup = BaseController.generateInlineButtons(buttons)

            bot.send_message(
                message.chat.id, f"<b>{username}, нашел список организаций за которыми вы закреплены:</b>\n{orgLabelsStroke}\n<b>Все верно</b> ?", reply_markup=markup, parse_mode="html")

        # subscribe command handler
        @bot.message_handler(["subscribe", "unsubscribe"])
        def subscribtionCommand(message: Message) -> None:

            if BaseController.isPublicChat(message):
                return

            value = True if message.text == "/subscribe" else False

            __setUserSubscribtion(message.chat.id, value)

        # /reg callback handler
        @bot.callback_query_handler(func=lambda message: message.data.split("|")[0].find("reg:") == 0)
        def registrationInlineHandler(msg: CallbackQuery):
            payload = msg.data.split("|")
            chatId = msg.message.chat.id

            # cancel btn handle
            if payload[0] == 'reg:0':
                bot.clear_step_handler(msg.message)
                bot.send_message(chatId, "Регистрация отменена")

            # accept btn handle
            elif payload[0] == "reg:1":
                bot.send_chat_action(chatId, 'typing')

                try:
                    user = AstUserStorage.getAstUserModel(
                        AstUserModel.id == payload[1])

                    UserStorage.add({
                        "chatId": chatId,
                        "chatUserId": msg.from_user.id,
                        "astOrgId": payload[2],
                        "astUserId": user.id,
                        "username": user.username,
                        "email": user.email,
                    })

                    logging.getLogger('Application').info(
                        f"User registered: {user.email}")

                    bot.send_message(
                        chatId, f"{user.username}, регистрация выполнена")

                except IntegrityError as error:
                    bot.send_message(
                        chatId, 'Пользователь с таким email уже зарегистрирован')

                except Exception as error:
                    bot.send_message(chatId, "Что-то пошло не так")
                    appLog.exception(error)

            bot.edit_message_reply_markup(
                chatId, msg.message.id, reply_markup=None)

            bot.delete_message(chatId, msg.message.id)

        # subscribe callback handler
        @bot.callback_query_handler(lambda message: message.data.find("subscription") == 0)
        def unsubscribe(msg: CallbackQuery) -> None:
            __setUserSubscribtion(msg.message.chat.id, False)

        def __setUserSubscribtion(chatId: int, value: bool) -> None:
            text = "подписались на рассылку" if value is True else "отписались от рассылки"

            try:
                # if not UserStorage.isAdmin(chatId):
                #     return

                UserStorage.updateByFields(
                    [UserModel.chatId == chatId], {'isSubscriber': value})
                bot.send_message(chatId, f"Вы успешно {text}")

            except Exception as error:
                bot.send_message(chatId, "Что-то пошло не так")
                appLog.exception(error)

        @bot.message_handler(['purgeusr'])
        def purgeBlockedUsers(message: Message) -> None:
            if BaseController.isPublicChat(message):
                return

            try:
                if not UserStorage.isAdmin(message.chat.id):
                    return

                AstUserStorage.purgeAllBlockedUsers()
                bot.send_message(message.chat.id, "Успех")

            except Exception as error:
                bot.send_message(
                    message.chat.id, "Не удалось удалить пользователей")
                appLog.exception(error)
