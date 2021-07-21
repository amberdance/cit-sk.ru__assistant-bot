from db.AssistantDbContext import AssistantDbContext
from telebot import TeleBot


class Database:
    def initializeMessageHandler(bot: TeleBot, dbConnection: AssistantDbContext):
        @bot.message_handler(commands=['registration', 'reg'])
        def registerUser(message):
            bot.send_message(message.chat.id, "status ok")

        @bot.message_handler(commands=['userid'])
        def registerUser(message):
            bot.send_message(
                message.chat.id, f'User id is: {message.chat.id}')

        @bot.message_handler(func=lambda message: True)
        def all(message):
            bot.send_message(
                message.chat.id, f'User id is: {message.chat.id}')
