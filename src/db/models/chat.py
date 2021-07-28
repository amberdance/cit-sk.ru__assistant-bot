from datetime import datetime
from sqlalchemy import DateTime, Integer, Column, Boolean, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from ..context import TelegramBotDbContext

Base = declarative_base()


class ChatUserModel(Base):
    __tablename__ = 'users'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    astUserId = Column('astUserId', Integer, nullable=False, unique=True)
    chatId: int = Column('chatId', Integer, nullable=False)
    chatUserId: int = Column('chatUserId', Integer, nullable=False)
    astOrgId: int = Column('astOrgId', Integer)
    username: str = Column('username', VARCHAR)
    email: str = Column('email', VARCHAR)
    created: datetime = Column('created', DateTime(
        timezone=True), default=datetime.utcnow())
    modified: datetime = Column(
        'modified', DateTime, onupdate=datetime.utcnow())
    modifiedBy: int = Column('modifiedBy', Integer, default=None)
    isBlocked: bool = Column('isBlocked', Boolean, default=False)
    role: int = Column('role', Integer, default=1)

    def createTable() -> None:
        Base.metadata.create_all(TelegramBotDbContext().getEngine())
