import logging
from typing import Iterable, Tuple, Union, List
from sqlalchemy.exc import DatabaseError
from ..storage.base import BaseStorage
from ..models.chat import ChatUserModel, MessageModel
from ..context import TelegramBotDbContext


session = TelegramBotDbContext().getSession()
dbLog = logging.getLogger('Database')


class ChatUserStorage():

    @staticmethod
    def add(fields: dict) -> int:
        return BaseStorage.addRow(ChatUserModel(**fields), session)

    @staticmethod
    def updateModel() -> None:
        BaseStorage.updateRow(session)

    @staticmethod
    def updateByFields(filter: Iterable, fields: dict) -> None:
        BaseStorage.updateRowByFields(ChatUserModel, filter, fields, session)

    @staticmethod
    def delete(user: ChatUserModel) -> None:
        BaseStorage.deleteRow(user, session)

    @staticmethod
    def getFields(*fields: Tuple, filter: Iterable = [], join: Tuple = None) -> List:
        try:
            query = session.query(*fields)

            if join is not None:
                query = session.query.join(*join)

            return [row._asdict() for row in query.filter(*filter).all()]

        except DatabaseError as error:
            dbLog.exception(error)

    @staticmethod
    def getModel(*filter: tuple, ) -> Union[ChatUserModel, List[ChatUserModel]]:
        try:
            result = [row for row in session.query(
                ChatUserModel).filter(*filter).all()]

            return result[0] if len(result) == 1 else result

        except DatabaseError as error:
            dbLog.exception(error)

    @staticmethod
    def getOperatorId(chatId: int) -> int:
        return session.query(ChatUserModel.astUserId).filter(ChatUserModel.chatId == chatId).all()[0]['astUserId']

    @staticmethod
    def isUserRegistered(chatUserId) -> bool:
        return bool(ChatUserStorage.getFields(ChatUserModel.id, filter=[ChatUserModel.chatUserId == chatUserId]))

    @staticmethod
    def isAdmin(chatUserId: int) -> bool:
        return bool(ChatUserStorage.getFields(ChatUserModel.role, filter=[ChatUserModel.role == 1, ChatUserModel.chatUserId == chatUserId]))


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
