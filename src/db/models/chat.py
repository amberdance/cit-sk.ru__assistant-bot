from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import DateTime, Integer, Column, Boolean, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from ..context import TelegramBotDbContext

Base = declarative_base()


def createTable() -> None:
    Base.metadata.create_all(TelegramBotDbContext().getEngine())


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created: datetime = Column(DateTime(
        timezone=False), server_default=func.now())
    astUserId = Column(Integer, nullable=False, unique=True)
    chatId: int = Column(Integer, nullable=False)
    chatUserId: int = Column(Integer, nullable=False)
    astOrgId: int = Column(Integer)
    username: str = Column(VARCHAR)
    email: str = Column(VARCHAR, unique=True)
    isBlocked: bool = Column(Boolean, default=False)
    isSubscriber: bool = Column(Boolean, default=True)
    role: int = Column(Integer, default=0)


class MessageModel(Base):
    __tablename__ = 'messages'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    created: datetime = Column(DateTime(
        timezone=False), server_default=func.now())
    messageId: int = Column(Integer, nullable=False)
    chatId: int = Column(Integer, nullable=False)
    taskId: int = Column(Integer)
    isBot: int = Column(Boolean, default=True)
    text: str = Column(VARCHAR)
