from abc import ABC, abstractmethod
from typing import Any, List
from telebot import TeleBot
from telebot.types import Message


class BaseController(ABC):
    @abstractmethod
    def initializeMessageHandler(bot: TeleBot) -> None:
        ...

    def sendMessage(bot: TeleBot, message: Message, data: Any):
        """Отправляет сообщение в лс, если боту пишут в группе, и в общий чат, если пишут в лс"""

        bot.send_message(message.chat.id, data) if(
            message.chat.type == 'private') else bot.reply_to(message, data)
