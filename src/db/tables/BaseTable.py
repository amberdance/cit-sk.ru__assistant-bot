from typing import overload
from sqlalchemy.orm import Session


class BaseTable:

    @staticmethod
    @overload
    def insertSingleRow(mappedClass: object, session: Session) -> None:
        session.add(mappedClass)
        session.commit()

    @staticmethod
    @overload
    def insertSingleRow(mappedClass: object, dbContext: str) -> None:
        from db.context.DbContextBase import DbContextBase

        session = DbContextBase(context=dbContext).getSession()
        session.add(mappedClass)
        session.commit()
