from typing import Union
from .BaseTable import BaseTable
from ..models.ChatUserModel import ChatUserModel
from ..context.TelegramBotDbContext import TelegramBotDbContext

session = TelegramBotDbContext().getSession()


class ChatUserTable(BaseTable):

    @staticmethod
    def getUserFields(*fields: property, filter: list = None) -> list:
        """Return dictionary data representaion"""

        return [row._asdict() for row in session.query(*fields).all()] if filter is None else [row._asdict() for row in session.query(*fields).filter(*filter).all()]

    @staticmethod
    def getUserModel(*filter: property) -> Union[ChatUserModel, list[ChatUserModel]]:
        """Return ORM model"""

        result = [row for row in session.query(ChatUserModel).all()] if filter is None else [
            row for row in session.query(ChatUserModel).filter(*filter).all()]

        return result[0] if len(result) == 1 else result

    @ staticmethod
    def addUser(user: ChatUserModel) -> ChatUserModel:
        BaseTable._insertRow(user, session=session)

        return user

    @staticmethod
    def updateUser() -> None:
        BaseTable._updateRow(session)

    @staticmethod
    def deleteUser(user: ChatUserModel) -> None:
        BaseTable._deleteRow(user, session)

    @staticmethod
    def isUserRegistered(chatUserId: int) -> bool:
        return bool(ChatUserTable.getUserFields(ChatUserModel.id, filter=[ChatUserModel.chatUserId == chatUserId]))

    @staticmethod
    def isAdmin(chatUserId: int) -> bool:
        return bool(ChatUserTable.getUserFields(ChatUserModel.role, filter=[ChatUserModel.chatUserId == chatUserId]))
