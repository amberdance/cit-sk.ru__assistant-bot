from .BaseTable import BaseTable
from ..models.UserModel import UserModel
from ..TelegramBotDatabase import TelegramBotDatabase


class UserTable(BaseTable):
    
    def addUser(user: UserModel):
        BaseTable._insertSingleRow(
            user, TelegramBotDatabase().getSession())
