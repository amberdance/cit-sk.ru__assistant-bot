import re
from sqlalchemy.exc import IntegrityError
from telebot.apihelper import ApiTelegramException
from telebot.types import CallbackQuery
from controllers.base import BaseController, TeleBot, Message, InlineKeyboardButton, appLog
from db.storage.chat import ChatUserStorage, ChatUserModel
from db.storage.assistant import AstUserStorage, AstUserModel, AstOrgUserModel


class ChatUserHandler:
    def initialize(bot: TeleBot):

        @bot.message_handler(["reg"])
        def stepOne(message: Message):

            if BaseController.isPublicChat(message):
                return

            chatId = message.chat.id

            if(ChatUserStorage.isUserRegistered(message.from_user.id)):
                username = ChatUserStorage.getFields(
                    ChatUserModel.username, filter=[ChatUserModel.chatUserId == message.from_user.id])[0]['username']

                return bot.send_message(chatId, f"{username}, Вы уже зарегистрированы")

            message = bot.send_message(
                chatId, "Введите логин вашей учетной записи в ассистенте")

            bot.register_next_step_handler(message, stepTwo)

        def stepTwo(message: Message) -> None:
            email = message.text

            if(message.text == "/cancel"):
                return bot.clear_step_handler_by_chat_id(message.chat.id)

            if(bool(re.findall(r'[\w\.-]+@[\w\.-]+(?:\.[\w]+)+', email)) is False):
                bot.send_message(message.chat.id, 'Введите корректный email')

                return bot.register_next_step_handler(message, stepTwo)

            organizationList = AstUserStorage.getOrganization(
                AstUserModel.email == email.lower(), AstOrgUserModel.status == 1)

            if(bool(organizationList) is False):
                bot.send_message(
                    message.chat.id, f'Пользователь с логином <b>{email}</b> не найден, попробуйте другой', parse_mode="html")

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
                bot.send_message(chatId, "Ладно, в другой раз")

            # accept btn handle
            elif payload[0] == "reg:1":
                bot.send_chat_action(chatId, 'typing')

                try:
                    user = AstUserStorage.getAstUserModel(
                        AstUserModel.id == payload[1])

                    ChatUserStorage.add({
                        "chatId": chatId,
                        "chatUserId": msg.from_user.id,
                        "astOrgId": payload[2],
                        "astUserId": user.id,
                        "username": user.username,
                        "email": user.email,
                    })

                    bot.send_message(
                        chatId, f"{user.username}, регистрация выполнена")

                except IntegrityError as error:
                    bot.send_message(
                        chatId, 'Пользователь с таким email уже зарегистрирован')

                except ApiTelegramException as error:
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
                if not ChatUserStorage.isAdmin(chatId):
                    return

                ChatUserStorage.updateByFields(
                    [ChatUserModel.chatId == chatId], {'isSubscriber': value})
                bot.send_message(chatId, f"Вы успешно {text}")

            except ApiTelegramException as error:
                appLog.exception(error)
                bot.send_message(chatId, "Что-то пошло не так")
