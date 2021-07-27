from datetime import datetime
from sqlalchemy import Column, VARCHAR, Integer, TIMESTAMP, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import false
from sqlalchemy.sql.schema import ForeignKey


Base = declarative_base()


class TaskModel(Base):
    __tablename__ = 'asttasks'

    id: int = Column('id', Integer, primary_key=True, autoincrement=True)
    deviceId: int = Column('deviceid', Integer,
                           ForeignKey('astclientdevices.id'))
    status: int = Column('status', Integer)
    clientOrgId: int = Column('clientorgid', Integer,
                              ForeignKey("astclientorgs.id"))
    userId: int = Column('userid', Integer)
    orderDate: datetime = Column('orderdate', TIMESTAMP)
    descr: str = Column('descr', VARCHAR)
    serviceStartData: datetime = Column(
        'servicestartdata', TIMESTAMP(timezone=False))
    serviceEndData: datetime = Column(
        'serviceenddata', TIMESTAMP(timezone=False))
    modDate: datetime = Column('moddate', TIMESTAMP(
        timezone=True), onupdate=datetime.utcnow())
    serviceDescr: str = Column('servicedescr', VARCHAR)
    operatorId: int = Column('operatorid', Integer, ForeignKey('astusers.id'))
    operatorOrgId: int = Column('operatororgid', Integer)
    categoryId: int = Column('categoryid', Integer)


class AstUserModel(Base):
    __tablename__ = 'astusers'

    id: int = Column('id', Integer,  primary_key=True, autoincrement=True)
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
    status: int = Column('status', Integer)


class OrganizationModel(Base):
    __tablename__ = 'astclientorgs'

    id: int = Column('id', Integer, primary_key=True, autoincrement=True)
    ownerId: int = Column('ownerid', Integer, ForeignKey('astusers.id'))
    title: int = Column('title', VARCHAR)
    email: int = Column('email', VARCHAR)
    address: str = Column('address', VARCHAR)
    phone: datetime = Column('phone', VARCHAR)
    code: datetime = Column('code', VARCHAR)
    isService: str = Column('isservice', Integer)
    status: int = Column('status', Integer)
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
