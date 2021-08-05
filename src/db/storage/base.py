import logging
from typing import Iterable
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import DatabaseError

dbLog = logging.getLogger('Database')


class BaseStorage:

    @staticmethod
    def addRow(model: object, session: Session) -> int:
        try:
            session.add(model)
            session.commit()

            return model.id

        except DatabaseError as error:
            session.rollback()
            dbLog.exception(error)

            raise

    @staticmethod
    def updateRow(session: Session) -> None:
        try:
            session.commit()

        except DatabaseError as error:
            session.rollback()
            dbLog.exception(error)

            raise

    @staticmethod
    def updateRowByFields(model: object, filter: Iterable, fields: dict, session: Session) -> None:
        try:
            session.query(model).filter(*filter).update(fields)
            session.commit()

        except DatabaseError as error:
            session.rollback()
            dbLog.exception(error)

            raise

    @staticmethod
    def deleteRow(model: object, session: Session) -> None:
        try:
            session.delete(model)
            session.commit()

        except DatabaseError as error:
            session.rollback()
            dbLog.exception(error)

            raise

    @staticmethod
    def deleteRowByFilter(model: object, filter: Iterable, session: Session) -> bool:
        try:
            session.query(model).filter(*filter).delete()
            session.commit()

            return True

        except DatabaseError as error:
            session.rollback()
            dbLog.exception(error)

            return False
