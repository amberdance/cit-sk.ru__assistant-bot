from abc import ABC, abstractmethod
from db.context.DbContextBase import DbContextBase
from telebot import TeleBot


class BaseController(ABC):

    @staticmethod
    @abstractmethod
    # To do: что передавать во второй параметр: контекст бд или только соединение с бд
    def initializeMessageHandler(bot: TeleBot, dbContext: DbContextBase = None):
        pass
