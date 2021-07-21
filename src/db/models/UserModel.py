from sqlalchemy import DateTime, Integer, Column, Boolean
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.declarative import declarative_base
from ..TelegramBotDatabase import TelegramBotDatabase
from datetime import datetime

Base = declarative_base()


class UserModel(Base):
    __tablename__ = 'users'

    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    astUserId = Column('astUserId', Integer, nullable=False)
    chatUserId = Column('chatUserId', Integer, nullable=False)
    created = Column('created', DateTime(
        timezone=True), default=datetime.utcnow())
    modified = Column('modified', DateTime, onupdate=datetime.utcnow())
    modifiedBy = Column('modifiedBy', Integer, default=None)
    isBlocked = Column('isBlocked', Boolean, default=False)
    role = Column('role', Integer, default=1)

    def __init__(self, astUserId, chatUserId, role):
        self.astUserId = astUserId
        self.chatUserId = chatUserId
        self.role = role

    def __repr__(self):
        return "<UserModel(userId='%s')>" % (self.chatUserId)

    def createTable():
        Base.metadata.create_all(TelegramBotDatabase().getEngine())
