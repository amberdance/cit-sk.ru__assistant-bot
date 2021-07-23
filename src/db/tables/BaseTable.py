from typing import Union, overload
from db.context.DbContextBase import DbContextBase, Session


class BaseTable:

    @staticmethod
    @overload
    def insertRow(model: object, session: Session) -> None:
        ...

    @staticmethod
    @overload
    def insertRow(model: object, context: str) -> None:
        ...

    @staticmethod
    @overload
    def updateRow(session: Session) -> None:
        ...

    @staticmethod
    @overload
    def updateRow(context: str) -> None:
        ...

    @staticmethod
    @overload
    def deleteRow(model: object, session: Session) -> None:
        ...

    @staticmethod
    @overload
    def deleteRow(model: object, context: str) -> None:
        ...

    @staticmethod
    def getRow(session: Session, *model: object,  filter: list[property]) -> Union[object, list[object]]:
        """Return ORM model"""

        result = [row for row in session.query(*model).all()] if filter is None else [
            row for row in session.query(*model).filter(*filter).all()]

        return result[0] if len(result) == 1 else result

    @staticmethod
    def insertRow(model: object, session: Session = None, context: str = None) -> None:
        if session is None:
            session = DbContextBase().getContext(context=context).getSession()

        session.add(model)
        session.commit()

    @staticmethod
    def updateRow(session: Session = None, context: str = None):
        if session is None:
            session = DbContextBase().getContext(context=context).getSession()

        session.commit()

    @staticmethod
    def deleteRow(model: object, session: Session = None, context: str = None):
        if session is None:
            session = DbContextBase().getContext(context=context).getSession()

        session.delete(model)
        session.commit()
