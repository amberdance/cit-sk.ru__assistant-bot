from .BaseTable import BaseTable
from ..models.ChatUserModel import ChatUserModel
from ..context.TelegramBotDbContext import TelegramBotDbContext


class ChatUserTable(BaseTable):

    @staticmethod
    def addUser(user: ChatUserModel) -> ChatUserModel:
        BaseTable.insertSingleRow(
            user, session=TelegramBotDbContext().getSession())

        return user
