from typing import overload
from db.context.DbContextBase import DbContextBase, Session


class BaseTable:

    @staticmethod
    @overload
    def insertSingleRow(mappedClass: object, session: Session) -> None:
        pass

    @staticmethod
    @overload
    def insertSingleRow(mappedClass: object, context: str) -> None:
        pass

    @staticmethod
    def insertSingleRow(mappedClass: object, session: Session = None, context: str = None) -> None:
        if session is None:
            session = DbContextBase().getContext(context=context).getSession()

        session.add(mappedClass)
        session.commit()
