from abc import ABC, abstractmethod
from db.AssistantDbContext import AssistantDbContext
from telebot import TeleBot


class CommandsBase(ABC):

    @staticmethod
    @abstractmethod
    def initializeMessageHandler(bot: TeleBot, dbConnection: AssistantDbContext = None):
        pass
