from datetime import datetime
from sqlalchemy import Column, VARCHAR, Integer, TIMESTAMP, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import column_property


Base = declarative_base()


class TaskModel(Base):
    __tablename__ = 'asttasks'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    deviceId: int = Column('deviceid', Integer,
                           ForeignKey('astclientdevices.id'))
    status: int = Column(Integer)
    clientOrgId: int = Column('clientorgid', Integer,
                              ForeignKey("astclientorgs.id"))
    userId: int = Column('userid', Integer)
    orderDate: datetime = Column('orderdate', TIMESTAMP)
    descr: str = Column('descr', VARCHAR)
    serviceStartData: datetime = Column(
        'servicestartdata', TIMESTAMP(timezone=False))
    serviceEndData: datetime = Column(
        'serviceenddata', TIMESTAMP(timezone=False))
    origdate:datetime = Column('moddate', TIMESTAMP(timezone=True), onupdate=datetime.utcnow())
    modDate: str = column_property(func.to_char(origdate, 'YYYY-MM-DD HH24:MI:SS'))
    serviceDescr: str = Column('servicedescr', VARCHAR)
    operatorId: int = Column('operatorid', Integer, ForeignKey('astusers.id'))
    operatorOrgId: int = Column('operatororgid', Integer)
    categoryId: int = Column('categoryid', Integer)


class AstUserModel(Base):
    __tablename__ = 'astusers'

    id: int = Column(Integer,  primary_key=True, autoincrement=True)
    uid: str = Column(VARCHAR)
    email: str = Column(VARCHAR)
    phone: str = Column(VARCHAR)
    username: str = Column(VARCHAR)
    status: int = Column(Integer)


class AstOrgUserModel(Base):
    __tablename__ = 'astclientorgusers'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    orgId: int = Column('orgid', Integer, ForeignKey('astclientorgs.id'))
    userId: int = Column('userid', Integer, ForeignKey('astusers.id'))
    status: int = Column(Integer)


class OrganizationModel(Base):
    __tablename__ = 'astclientorgs'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    ownerId: int = Column('ownerid', Integer, ForeignKey('astusers.id'))
    title: int = Column(VARCHAR)
    email: int = Column(VARCHAR)
    address: str = Column(VARCHAR)
    phone: datetime = Column(VARCHAR)
    code: datetime = Column(VARCHAR)
    isService: str = Column('isservice', Integer)
    status: int = Column(Integer)
    isLogEnabled: int = Column('islogenabled', Integer)


class DeviceModel(Base):
    __tablename__ = 'astdevices'

    id: int = Column('id', Integer,  primary_key=True, autoincrement=True)
    status: int = Column('status', Integer)
    hid: str = Column('hid', VARCHAR)
    version: str = Column('version', VARCHAR)
    domainName: str = Column('domainname', VARCHAR)
    domainNameFull: str = Column('domainnamefull', VARCHAR)
    host: str = Column('host', VARCHAR)
    deleted: str = Column('deleted', Boolean)
    osName: str = Column('osfullname', VARCHAR)


class ClientDeviceModel(Base):
    __tablename__ = 'astclientdevices'

    id: int = Column('id', Integer, primary_key=True, autoincrement=True)
    orgId: int = Column('orgid', Integer, ForeignKey('astclientorgs.id'))
    userId: int = Column('userid', Integer, ForeignKey('astusers.id'))
    deviceId: int = Column('deviceid', Integer, ForeignKey('astdevices.id'))
    groupId: int = Column('groupid', Integer)
    title: str = Column('title', VARCHAR)
    description: str = Column('description', VARCHAR)
