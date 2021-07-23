from abc import ABC, abstractmethod
from typing import Any, List, Union
from telebot import TeleBot, types
from telebot.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message


class BaseController(ABC):
    @abstractmethod
    def initializeMessageHandler(bot: TeleBot) -> None:
        ...

    def genMarkup():
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton("Yes", callback_data="cb_yes"))
        markup.add(InlineKeyboardButton("No", callback_data="cb_no"))

        return markup

    def sendMessage(bot: TeleBot, message: Union[Message, CallbackQuery],  text: Any, parseMode: str = None):
        """Отправляет сообщение в лс, если боту пишут в группе, и в общий чат, если пишут в лс"""
        #to do: у CallbackQuery поле chat в message
        bot.send_message(message.chat.id, text, parse_mode=parseMode) if(message.chat.type == 'private') else bot.send_message(message.from_user.id, text, parse_mode=parseMode)
