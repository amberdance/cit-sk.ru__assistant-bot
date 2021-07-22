from db.models.ChatUserModel import Base, ChatUserModel
from db.tables.ChatUserTable import ChatUserTable
from .BaseController import BaseController, TeleBot
from config import IS_DEBUG_MODE


class DatabaseCommandsController(BaseController):

    @staticmethod
    def initializeMessageHandler(bot: TeleBot) -> None:
        @bot.message_handler(commands=['register', 'reg'])
        def registerUserCommand(message):

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

        @bot.message_handler(commands=['debugmsg'])
        def debugMessage(message):
            BaseController.sendMessage(bot, message, message)
