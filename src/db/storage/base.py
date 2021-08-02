from typing import Iterable
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import DatabaseError


class BaseStorage:

    @staticmethod
    def addRow(model: object, session: Session) -> int:
        try:
            session.add(model)
            session.commit()

            return model.id

        except DatabaseError:
            session.rollback()

            raise

    @staticmethod
    def updateRow(session: Session) -> None:
        try:
            session.commit()

        except DatabaseError:
            session.rollback()

            raise

    @staticmethod
    def updateRowByFields(model: object, filter: Iterable, fields: dict, session: Session) -> None:
        try:
            session.query(model).filter(*filter).update(fields)
            session.commit()

        except DatabaseError:
            session.rollback()

            raise

    @staticmethod
    def deleteRow(model: object, session: Session) -> None:
        try:
            session.delete(model)
            session.commit()

        except DatabaseError:
            session.rollback()

            raise
