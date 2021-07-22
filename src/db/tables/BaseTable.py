from typing import overload
from db.context.DbContextBase import DbContextBase, Session


class BaseTable:

    @staticmethod
    @overload
    def _insertRow(mappedClass: object, session: Session) -> None:
        ...

    @staticmethod
    @overload
    def _insertRow(mappedClass: object, context: str) -> None:
        ...

    @staticmethod
    @overload
    def _updateRow(session: Session) -> None:
        ...

    @staticmethod
    @overload
    def _updateRow(context: str) -> None:
        ...

    @staticmethod
    @overload
    def _deleteRow(mappedClass: object, session: Session) -> None:
        ...

    @staticmethod
    @overload
    def _deleteRow(mappedClass: object, context: str) -> None:
        ...

    @staticmethod
    def _insertRow(mappedClass: object, session: Session = None, context: str = None) -> None:
        if session is None:
            session = DbContextBase().getContext(context=context).getSession()

        session.add(mappedClass)
        session.commit()

    @staticmethod
    def _updateRow(session: Session = None, context: str = None):
        if session is None:
            session = DbContextBase().getContext(context=context).getSession()

        session.commit()

    @staticmethod
    def _deleteRow(mappedClass: object, session: Session = None, context: str = None):
        if session is None:
            session = DbContextBase().getContext(context=context).getSession()

        session.delete(mappedClass)
        session.commit()
