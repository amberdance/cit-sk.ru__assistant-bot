from typing import Any
from sqlalchemy import create_engine, text
from sqlalchemy.engine.base import Connection, Engine
from sqlalchemy.orm.session import Session, sessionmaker


class DbContextBase:
    _engine = None
    _connection = None
    _session = None

    def __init__(self, host, login, password, db) -> None:
        if self._engine is None:
            self._engine = create_engine(
                f'postgresql+psycopg2://{login}:{password}@{host}/{db}')

        if self._connection is None:
            self._connection = self._engine.connect()

        if self._session is None:
            Session = sessionmaker()
            Session.configure(bind=self._engine)
            self._session = Session()

    def getEngine(self) -> Engine:
        return self._engine

    def getConnection(self) -> Connection:
        return self._connection

    def getSession(self) -> Session:
        return self._session

    def closeConnection(self) -> None:
        self._connection.close()
        self._connection = None

    def closeSession(self) -> None:
        self._session.close_all()
        self._session = None

    def rawQuery(self, queryString) -> Any:
        return self._connection.execute(text(queryString)).fetchall()
