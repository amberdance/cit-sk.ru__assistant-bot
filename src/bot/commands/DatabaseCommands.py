from .CommandsBase import CommandsBase


class DatabaseCommands(CommandsBase):
    def initializeMessageHandler(bot, dbConnection):
        @bot.message_handler(commands=['registration', 'reg'])
        def registerUser(message):
            bot.send_message(message.chat.id, "status ok")

        @bot.message_handler(func=lambda message: True)
        def all(message):
            bot.send_message(
                message.chat.id, f'User Id is: {message.chat.id}')
