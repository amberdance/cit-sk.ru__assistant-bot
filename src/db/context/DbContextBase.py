from typing import Any, overload
from sqlalchemy import create_engine, text
from sqlalchemy.engine.base import Connection, Engine
from sqlalchemy.orm.session import Session, sessionmaker


class DbContextBase:

    _engine: Engine = None
    _connection: Connection = None
    _session: Session = None

    # To do: подумать над аргументом context, нужен или нет.
    def __init__(self, host: str = None, login: str = None, password: str = None, db: str = None, context: str = None) -> None:
        if context is not None:
            config = self.__getDatabaseConfig(context)

            self._engine = create_engine(
                f'postgresql+psycopg2://{config["LOGIN"]}:{config["PASSWORD"]}@{config["HOST"]}/{config["DB"]}')

        else:
            self._engine = create_engine(
                f'postgresql+psycopg2://{login}:{password}@{host}/{db}')

        if self._connection is None:
            self._connection = self._engine.connect()

        if self._session is None:
            Session = sessionmaker(expire_on_commit=False)
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

    @staticmethod
    def __getDatabaseConfig(context: str) -> dict:
        from config import TELEGRAMBOT_DB, ASSISTANT_DB

        if context == "telegram":
            return TELEGRAMBOT_DB

        if context == "assistant":
            return ASSISTANT_DB
