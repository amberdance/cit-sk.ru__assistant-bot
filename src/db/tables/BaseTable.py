from sqlalchemy.orm import Session


class BaseTable:

    @staticmethod
    def _insertSingleRow(mappedClass: object, session: Session) -> None:
        session.add(mappedClass)
        session.commit()
