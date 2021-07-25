from typing import Union, List
from sqlalchemy.engine.row import Row
from .BaseTable import BaseTable
from ..models.chat import ChatUserModel
from ..context import TelegramBotDbContext

session = TelegramBotDbContext().getSession()


class ChatUserTable(BaseTable):

    @staticmethod
    def getUserFields(*fields: property, filter: list = [], join: list = None) -> Union[Row, List[Row]]:
        query = session.query(*fields)

        if join is not None:
            query = query.join(*join)

        result = query.filter(*filter).all()

        return result[0] if len(result) == 1 else result

    @staticmethod
    def getUserModel(*filter: property) -> Union[ChatUserModel, List[ChatUserModel]]:
        result = [row for row in session.query(
            ChatUserModel).filter(*filter).all()]

        return result[0] if len(result) == 1 else result

    @ staticmethod
    def addUser(user: ChatUserModel) -> ChatUserModel:
        BaseTable.insertRow(user, session=session)

        return user

    @staticmethod
    def updateUser() -> None:
        BaseTable.updateRow(session)

    @staticmethod
    def deleteUser(user: ChatUserModel) -> None:
        BaseTable.deleteRow(user, session)

    @staticmethod
    def isUserRegistered(chatUserId: int) -> bool:
        return bool(ChatUserTable.getUserFields(ChatUserModel.id, filter=[ChatUserModel.chatUserId == chatUserId]))

    @staticmethod
    def isAdmin(chatUserId: int) -> bool:
        return bool(ChatUserTable.getUserFields(ChatUserModel.role, filter=[ChatUserModel.role == 1, ChatUserModel.chatUserId == chatUserId]))
