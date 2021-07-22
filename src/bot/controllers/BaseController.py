from abc import ABC, abstractmethod
from typing import Any
from telebot import TeleBot
from telebot.types import Message


class BaseController(ABC):
    @abstractmethod
    def initializeMessageHandler(bot: TeleBot) -> None:
        ...

    def sendMessage(bot: TeleBot, message: Message, data: Any):
        """Отправляет сообщение в reply, если в находится группе, и в чат, если в лс"""

        bot.send_message(message.chat.id, data) if(
            message.chat.type == 'private') else bot.reply_to(message, data)
