from db.models.ChatUserModel import ChatUserModel
from db.tables.ChatUserTable import ChatUserTable
from .BaseController import BaseController, TeleBot
from config import IS_DEBUG_MODE


class DatabaseCommandsController(BaseController):

    @staticmethod
    def initializeMessageHandler(bot: TeleBot) -> None:
        @bot.message_handler(commands=['registration', 'reg'])
        def registerUserCommand(message):
            try:
                if(ChatUserTable.isUserRegistered(message.from_user.id)):
                    bot.send_message(
                        # to do: распознать пол
                        message.chat.id, f"{message.from_user.first_name} {message.from_user.last_name}, ранее Вы уже были зарегистрированы. Чтобы узнать Ваш id введите /userid")
                else:
                    fields = {
                        "astUserId": 1,
                        "chatUserId": message.from_user.id
                    }

                    ChatUserTable.addUser(ChatUserModel(**fields))

                    bot.send_message(
                        message.chat.id, "Регистрация прошла успешно! Чтобы узнать свой id напишите команду /userid")
            except Exception as error:
                errorMsg = "К сожалению, не удалось вас зарегистрировать, попробуйте еще раз" if IS_DEBUG_MODE is False else error
                bot.send_message(message.chat.id, errorMsg)
