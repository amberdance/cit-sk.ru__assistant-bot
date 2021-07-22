from datetime import datetime
from sqlalchemy import DateTime, Integer, Column, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TaskModel(Base):
    __tablename__ = 'asttasks'
