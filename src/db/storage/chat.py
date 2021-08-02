from typing import Iterable, Tuple, Union, List
from ..storage.base import BaseStorage
from ..models.chat import ChatUserModel, MessageModel
from ..context import TelegramBotDbContext


session = TelegramBotDbContext().getSession()


class ChatUserStorage():

    @ staticmethod
    def add(fields: dict) -> int:
        return BaseStorage.addRow(ChatUserModel(**fields), session)

    @staticmethod
    def update() -> None:
        BaseStorage.updateRow(session)

    @staticmethod
    def updateByFields(filter: Iterable, fields: dict) -> None:
        BaseStorage.updateRowByFields(ChatUserModel, filter, fields, session)

    @staticmethod
    def delete(user: ChatUserModel) -> None:
        BaseStorage.deleteRow(user, session)

    @staticmethod
    def getUserFields(*fields: Tuple, filter: Iterable = [], join: Tuple = None) -> List:
        query = session.query(*fields)

        if join is not None:
            query = session.query.join(*join)

        return [row._asdict() for row in query.filter(*filter).all()]

    @staticmethod
    def getUser(*filter: tuple, ) -> Union[ChatUserModel, List[ChatUserModel]]:
        result = [row for row in session.query(
            ChatUserModel).filter(*filter).all()]

        return result[0] if len(result) == 1 else result

    @staticmethod
    def isUserRegistered(chatUserId) -> bool:
        return bool(ChatUserStorage.getUserFields(ChatUserModel.id, filter=[ChatUserModel.chatUserId == chatUserId]))

    @staticmethod
    def isAdmin(chatUserId: int) -> bool:
        return bool(ChatUserStorage.getUserFields(ChatUserModel.role, filter=[ChatUserModel.role == 1, ChatUserModel.chatUserId == chatUserId]))


class MessageStorage:

    @staticmethod
    def add(fields: dict) -> int:
        return BaseStorage.addRow(MessageModel(**fields), session)

    @staticmethod
    def delete(message: object) -> None:
        BaseStorage.deleteRow(message, session)

    @staticmethod
    def delete(id: object) -> None:
        BaseStorage.deleteRow(id, session)

    @staticmethod
    def getByTaskId(id: int) -> List[MessageModel]:
        return session.query(MessageModel).filter(MessageModel.taskId == id).all()
