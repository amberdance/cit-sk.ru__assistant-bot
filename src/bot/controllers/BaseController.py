from abc import ABC, abstractmethod
from telebot import TeleBot


class BaseController(ABC):
    @abstractmethod
    def initializeMessageHandler(bot: TeleBot) -> None:
        ...
