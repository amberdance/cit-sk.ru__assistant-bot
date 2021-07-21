import re
from sqlalchemy.sql.expression import text
from db.context.DbContextBase import DbContextBase
from .BaseController import BaseController
from telebot import TeleBot


class DatabaseCommandsController(BaseController):

    @staticmethod
    def initializeMessageHandler(bot: TeleBot) -> None:
        @bot.message_handler(commands=['registration', 'reg'])
        def registerUserCommand(message):
            bot.reply_to(message, "status ok")

        @bot.message_handler(commands=["test"])
        def testCommand(message):
            session = DbContextBase(context="assistant").getSession()
            someDataFromDatabase = session.execute(
                text("select id, orderdate, descr from asttasks order by random() desc limit 1"))
            result = {}
            for row in someDataFromDatabase:
                result = dict(row)

            bot.reply_to(
                message, f"Выборка рандомной заявки: {result['id']}, неисправность: {result['descr']}, дата создания: {result['orderdate']}")

        # @bot.message_handler(func=lambda message: True)
        # def echoAllCommand(message) -> None:
        #     bot.reply_to(
        #         message, "Command not supported")
