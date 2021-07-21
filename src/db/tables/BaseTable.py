from typing import overload
from sqlalchemy.orm import Session
from db.context.DbContextBase import DbContextBase


class BaseTable:

    @staticmethod
    @overload
    def insertSingleRow(mappedClass: object, session: Session) -> None:
        session.add(mappedClass)
        session.commit()

    @staticmethod
    @overload
    def insertSingleRow(mappedClass: object, dbContext: str) -> None:
        session = DbContextBase(context=dbContext).getSession()
        session.add(mappedClass)
        session.commit()
