from sqlalchemy.orm import Session


class BaseTable:

    @staticmethod
    def _insertSingleRow(mappedClass: object, session: Session):
        session.add(mappedClass)
        session.commit()
