from datetime import datetime
from sqlalchemy import Text, Integer, Column, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TaskModel(Base):
    __tablename__ = 'asttasks'

    id: int = Column('id', Integer(), primary_key=True, autoincrement=True)
    status: int = Column('status', Integer)
    clientOrgId: int = Column('clientorgid', Integer)
    userId: int = Column('userid', Integer)
    orderDate: datetime = Column('orderdate', TIMESTAMP(
        timezone=True), default=datetime.utcnow())
    descr: str = Column('descr', Text)
    serviceStartData: datetime = Column('servicestartdata')
    serviceEndData: datetime = Column('serviceenddata')
    serviceDescr: str = Column('servicedescr', Text)
    operatorId: int = Column('operatorid', Integer)
    operatorOrgId: int = Column('operatororgid', Integer)
    categoryId: int = Column('categoryid', Integer)
