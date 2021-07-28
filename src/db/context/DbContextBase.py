from typing import overload
import logging
from sqlalchemy.engine import create_engine
from sqlalchemy.engine.base import Connection, Engine
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm.session import Session, sessionmaker
from config import ASSISTANT_DB, TELEGRAM_DB


class DbContextBase:

    _engine: Engine = None
    _connection: Connection = None
    _session: Session = None

    @overload
    def getContext(self, context: str):
        pass

    @overload
    def getContext(self, host: str, login: str, password: str, db: str):
        pass

    def getContext(self, host: str = None, login: str = None, password: str = None, db: str = None, context: str = None):
        """ return DbContextBase """
        if isinstance(context, str):
            config = self.__getDatabaseConfig(context)
            self._engine = create_engine(
                f'postgresql+psycopg2://{config["LOGIN"]}:{config["PASSWORD"]}@{config["HOST"]}/{config["DB"]}', pool_pre_ping=True, pool_recycle=30)
        else:
            self._engine = create_engine(
                f'postgresql+psycopg2://{login}:{password}@{host}/{db}', pool_pre_ping=True, pool_recycle=30)

        self.__createConnection()
        self.__createSession()

        return self

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

    def __createConnection(self) -> None:
        self._connection = self._engine.connect()

    def __createSession(self) -> None:
        session = sessionmaker()
        session.configure(bind=self._engine)
        self._session = session()

    @staticmethod
    def __getDatabaseConfig(context: str) -> dict:
        if context == "telegram":
            return TELEGRAM_DB

        if context == "assistant":
            return ASSISTANT_DB
