from typing import Union
from .BaseTable import BaseTable
from ..models.chat import UserModel
from ..context.TelegramBotDbContext import TelegramBotDbContext

session = TelegramBotDbContext().getSession()


class UserTable(BaseTable):

    @staticmethod
    def getUserFields(*fields: property, filter: list = None) -> list:
        """Return dictionary data representaion"""

        return [row._asdict() for row in session.query(*fields).all()] if filter is None else [row._asdict() for row in session.query(*fields).filter(*filter).all()]

    @staticmethod
    def getUserModel(*filter: property) -> Union[UserModel, list[UserModel]]:
        """Return ORM model"""

        result = [row for row in session.query(UserModel).all()] if filter is None else [
            row for row in session.query(UserModel).filter(*filter).all()]

        return result[0] if len(result) == 1 else result

    @ staticmethod
    def addUser(user: UserModel) -> UserModel:
        BaseTable.insertRow(user, session=session)

        return user

    @staticmethod
    def updateUser() -> None:
        BaseTable.updateRow(session)

    @staticmethod
    def deleteUser(user: UserModel) -> None:
        BaseTable.deleteRow(user, session)

    @staticmethod
    def isUserRegistered(chatUserId: int) -> bool:
        return bool(UserTable.getUserFields(UserModel.id, filter=[UserModel.chatUserId == chatUserId]))

    @staticmethod
    def isAdmin(chatUserId: int) -> bool:
        return bool(UserTable.getUserFields(UserModel.role, filter=[UserModel.role == 1]))
