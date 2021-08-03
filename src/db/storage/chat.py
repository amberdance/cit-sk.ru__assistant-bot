
from typing import Iterable, Tuple, Union, List
from sqlalchemy.exc import SQLAlchemyError
from ..storage.base import BaseStorage, dbLog
from ..models.chat import UserModel, MessageModel
from ..context import TelegramBotDbContext


session = TelegramBotDbContext().getSession()


class UserStorage():

    @staticmethod
    def add(fields: dict) -> int:
        return BaseStorage.addRow(UserModel(**fields), session)

    @staticmethod
    def updateModel() -> None:
        BaseStorage.updateRow(session)

    @staticmethod
    def updateByFields(filter: Iterable, fields: dict) -> None:
        BaseStorage.updateRowByFields(UserModel, filter, fields, session)

    @staticmethod
    def delete(user: UserModel) -> None:
        BaseStorage.deleteRow(user, session)

    @staticmethod
    def getFields(*fields: Tuple, filter: Iterable = [], join: Tuple = None) -> List:
        try:
            query = session.query(*fields)

            if join is not None:
                query = session.query.join(*join)

            return [row._asdict() for row in query.filter(*filter).all()]

        except SQLAlchemyError as error:
            dbLog.exception(error)

    @staticmethod
    def getModel(*filter: tuple, ) -> Union[UserModel, List[UserModel]]:
        try:
            result = [row for row in session.query(
                UserModel).filter(*filter).all()]

            return result[0] if len(result) == 1 else result

        except SQLAlchemyError as error:
            dbLog.exception(error)

    @staticmethod
    def getUsers() -> List:
        return UserStorage.getFields(
            UserModel.id,
            UserModel.astUserId,
            UserModel.username,
            UserModel.chatId,
            UserModel.role,
            filter=[
                UserModel.isBlocked == False,
                UserModel.isSubscriber == True
            ])

    @staticmethod
    def getOperatorId(chatId: int) -> int:
        return session.query(UserModel.astUserId).filter(UserModel.chatId == chatId).all()[0]['astUserId']

    @staticmethod
    def isUserRegistered(chatId) -> bool:
        return bool(UserStorage.getFields(UserModel.id, filter=[UserModel.chatId == chatId]))

    @staticmethod
    def isAdmin(chatId: int) -> bool:
        return bool(UserStorage.getFields(UserModel.role, filter=[UserModel.role == 1, UserModel.chatId == chatId]))


class MessageStorage:

    @staticmethod
    def add(fields: dict) -> int:
        return BaseStorage.addRow(MessageModel(**fields), session)

    @staticmethod
    def updateModel() -> None:
        BaseStorage.updateRow(session)

    @staticmethod
    def updateByFields(id: int, fields: dict) -> None:
        BaseStorage.updateRowByFields(MessageModel, id, fields, session)

    @staticmethod
    def delete(id: object) -> None:
        BaseStorage.deleteRow(id, session)

    @staticmethod
    def getByTaskId(id: int) -> List[MessageModel]:
        return session.query(MessageModel).filter(MessageModel.taskId == id).all()
