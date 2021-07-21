from .BaseController import BaseController, TeleBot


class CommonCommandsController(BaseController):

    @staticmethod
    def initializeMessageHandler(bot: TeleBot) -> None:
        @bot.message_handler(commands=['help'])
        def helpCommand(message):
            bot.send_message(message.chat.id, "help here")
