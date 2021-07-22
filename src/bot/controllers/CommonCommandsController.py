from .BaseController import BaseController, TeleBot


class CommonCommandsController(BaseController):

    @staticmethod
    def initializeMessageHandler(bot: TeleBot) -> None:
        @bot.message_handler(commands=['help'])
        def helpCommand(message):

            htmlTemplate = "<b>Помощь</b>\n /help \n /userid - id пользователя"
            + "\n\n <b>Работа с заявками</b> \n /task - информация о заявке по ее номеру""

            bot.send_message(
                message.chat.id, parse_mode="html", text=htmlTemplate)
