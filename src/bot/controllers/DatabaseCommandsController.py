from sqlalchemy.sql.expression import text
from .BaseController import BaseController, TeleBot
from utils import formatResultSetToDict
from db.context.DbContextBase import DbContextBase


class DatabaseCommandsController(BaseController):

    @staticmethod
    def initializeMessageHandler(bot: TeleBot) -> None:

        @bot.message_handler(commands=['registration', 'reg'])
        def registerUserCommand(message):
            bot.reply_to(message, "status ok")

        @bot.message_handler(commands=["test"])
        def testCommand(message):
            session = DbContextBase().getContext(
                context="assistant").getSession()

            result = formatResultSetToDict(session.execute(
                text("select id, orderdate, descr from asttasks order by random() desc limit 1")))

            bot.reply_to(
                message, f"Рандомная заявка №{result['id']}, дата создания: {result['orderdate']}, неисправность: {result['descr']}")
