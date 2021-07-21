from .BaseTable import BaseTable
from ..models.UserModel import UserModel
from ..context.TelegramBotDbContext import TelegramBotDbContext


class UserTable(BaseTable):

    @staticmethod
    def addUser(user: UserModel) -> None:
        BaseTable._insertSingleRow(
            user, TelegramBotDbContext().getSession())
