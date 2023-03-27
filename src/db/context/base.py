from sqlalchemy.engine import create_engine
from sqlalchemy.engine.base import Connection, Engine
from sqlalchemy.orm.session import Session


class DbContextBase:
    __engine: Engine = None
    __connection: Connection = None
    __session: Session = None

    def __init__(self, host: str = None, login: str = None, password: str = None, db: str = None):
        self.__engine = create_engine(
            f'postgresql+psycopg2://{login}:{password}@{host}/{db}', pool_pre_ping=True, pool_recycle=30)

        self.__connection = self.__engine.connect()
        self.__session = Session(self.__engine)

        return self

    def getEngine(self) -> Engine:
        return self.__engine

    def getConnection(self) -> Connection:
        return self.__connection

    def getSession(self) -> Session:
        print(f'session created {self.__engine}')
        return self.__session

    def closeConnection(self) -> None:
        self.__connection.close()

    def closeSession(self) -> None:
        self.__session.close_all()
