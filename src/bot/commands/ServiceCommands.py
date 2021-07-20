from .CommonCommands import CommonCommands


class ServiceCommands(CommonCommands):

    def initializeMessageHandler(bot):
        @bot.message_handler(commands=['userid'])
        def registerUser(message):
            bot.send_message(
                message.chat.id, f'User id is: {message.chat.id}')
