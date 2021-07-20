from abc import ABC, abstractmethod
from dbLayer.AssistantDb import AssistantDb
from telebot import TeleBot


class CommandsBase(ABC):

    @staticmethod
    @abstractmethod
    def initializeMessageHandler(bot: TeleBot, dbConnection: AssistantDb = None):
        pass
