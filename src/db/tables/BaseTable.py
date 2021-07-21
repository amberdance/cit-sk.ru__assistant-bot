from typing import overload
from db.context.DbContextBase import DbContextBase, Session


class BaseTable:

    @staticmethod
    @overload
    def insertSingleRow(mappedClass: object, session: Session) -> None:
        session.add(mappedClass)
        session.commit()

    @staticmethod
    @overload
    def insertSingleRow(mappedClass: object, dbContext: str) -> None:
        session = DbContextBase.getContext(dbContext).getSession()
        session.add(mappedClass)
        session.commit()

    def insertSingleRow(mappedClass: object, session: Session = None, dbContext: str = None) -> None:
        if session is None:
            session = DbContextBase().getContext(dbContext).getSession()

        session.add(mappedClass)
        session.commit()
