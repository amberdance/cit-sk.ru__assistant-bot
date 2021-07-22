from datetime import datetime
from sqlalchemy import DateTime, Integer, Column, Boolean
from sqlalchemy.ext.declarative import declarative_base
from ..context.TelegramBotDbContext import TelegramBotDbContext

Base = declarative_base()


class ChatUserModel(Base):
    __tablename__ = 'users'

    id: int = Column('id', Integer(), primary_key=True, autoincrement=True)
    astUserId: int = Column('astUserId', Integer, nullable=False)
    chatUserId: int = Column('chatUserId', Integer, nullable=False)
    created: datetime = Column('created', DateTime(
        timezone=True), default=datetime.utcnow())
    modified: datetime = Column(
        'modified', DateTime, onupdate=datetime.utcnow())
    modifiedBy: int = Column('modifiedBy', Integer, default=None)
    isBlocked: bool = Column('isBlocked', Boolean, default=False)
    role: int = Column('role', Integer, default=1)

    def createTable() -> None:
        Base.metadata.create_all(TelegramBotDbContext().getEngine())
