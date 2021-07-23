from datetime import datetime
from sqlalchemy import Text, Integer, Column, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import VARCHAR


Base = declarative_base()


class TaskModel(Base):
    __tablename__ = 'asttasks'

    id: int = Column('id', Integer, primary_key=True, autoincrement=True)
    status: int = Column('status', Integer)
    clientOrgId: int = Column('clientorgid', Integer,
                              ForeignKey("astclientorgs.id"))
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


class AstUserModel(Base):
    __tablename__ = 'astusers'

    id: int = Column('id', Integer, primary_key=True, autoincrement=True)
    uid: str = Column('uid', VARCHAR)
    email: str = Column('email', VARCHAR)
    phone: str = Column('phone', VARCHAR)
    username: str = Column('username', VARCHAR)
    status: int = Column('status', Integer)


class AstOrgUserModel(Base):
    __tablename__ = 'astclientorgusers'

    id: int = Column('id', Integer, primary_key=True, autoincrement=True)
    orgId: int = Column('orgid', Integer, ForeignKey('astclientorgs.id'))
    userId: int = Column('userid', Integer, ForeignKey('astusers.id'))


class OrganizationModel(Base):
    __tablename__ = 'astclientorgs'

    id: int = Column('id', Integer, primary_key=True, autoincrement=True)
    ownerID: int = Column('ownerid', Integer)
    title: int = Column('title', VARCHAR)
    email: int = Column('email', VARCHAR)
    address: str = Column('address', VARCHAR)
    phone: datetime = Column('phone', VARCHAR)
    code: datetime = Column('code', VARCHAR)
    isService: str = Column('isservice', Integer)
    status: int = Column('status', Integer)
    isLogEnabled: int = Column('islogenabled', Integer)
