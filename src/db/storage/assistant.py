
from typing import Iterable, Union, List
from sqlalchemy.exc import OperationalError, DatabaseError
from sqlalchemy.engine.row import Row
from sqlalchemy.sql.expression import label
from ..context import AssistantDbContext
from ..storage.base import BaseStorage, dbLog
from ..storage.chat import *
from ..models.assistant import *


session = AssistantDbContext().getSession()


class AstUserStorage():

    @staticmethod
    def getOrganization(*filter: Iterable) -> List:
        if(bool(filter) is False):
            raise Exception("Filter parameter is required")

        fields = (
            OrganizationModel.id.label('orgId'),
            AstUserModel.id.label('userId'),
            OrganizationModel.title,
            AstOrgUserModel.id,
            AstUserModel.email,
            AstUserModel.username
        )

        try:
            return session.query(*fields).select_from(OrganizationModel).join(AstOrgUserModel, AstUserModel).filter(*filter).all()

        except DatabaseError as error:
            dbLog.exception(error)

    @staticmethod
    def getAstUserModel(*filter: Iterable) -> Union[AstUserModel, List[AstUserModel]]:

        if(bool(filter) is False):
            raise Exception("Filter parameter is required")

        try:
            result = session.query(AstUserModel).filter(*filter).all()

            return result[0] if len(result) == 1 else result

        except DatabaseError as error:
            dbLog.exception(error)

    @staticmethod
    def purgeAllBlockedUsers() -> None:
        BaseStorage.deleteRowByFilter(
            AstUserModel, [AstUserModel.status == 1], session)

        BaseStorage.deleteRowByFilter(
            AstOrgUserModel, [AstOrgUserModel.status == 0], session)


class TaskStorage():

    @staticmethod
    def updateModel() -> None:
        BaseStorage.updateRow(session)

    @staticmethod
    def updateByFields(id: int, fields: dict) -> None:
        BaseStorage.updateRowByFields(TaskModel, id, fields, session)

    @staticmethod
    def delete(task: TaskModel) -> None:
        BaseStorage.deleteRow(task, session)

    @staticmethod
    def getFields(*fields: List, filter: Iterable = None, join: Iterable = None) -> List:
        try:
            query = session.query(*fields).select_from(TaskModel)

            if join is not None:
                query = query.outerjoin(*join)

            return [row._asdict() for row in query.filter(*filter).all()]

        except DatabaseError as error:
            dbLog.exception(error)

    @staticmethod
    def getModel(*filter: List, join: Iterable = None) -> Union[TaskModel, List[TaskModel]]:
        try:
            query = session.query(TaskModel)

            if join is not None:
                query = query.join(*join)

            result = query.filter(*filter).order_by(TaskModel.id.desc()).all()

            return result[0] if len(result) == 1 else result

        except DatabaseError as error:
            dbLog.exception(error)

    @staticmethod
    def getByConditions(operatorId: int,  statusId: int = None, taskId: int = None,
                        limit: int = None, order: str = "asc", isUserAdmin=False) -> Union[List, Row]:

        queryFields = (
            TaskModel.id,
            TaskModel.descr,
            TaskModel.status,
            TaskModel.created.label('orderDate'),
            TaskModel.operatorOrgId.label('operatorOrgId'),
            TaskModel.serviceDescr,
            DeviceModel.hid,
            ClientDeviceModel.title.label('client'),
            OrganizationModel.title.label("org"),
            AstUserModel.username.label('operator')
        )

        filter = []

        if statusId is not None:
            filter.append(TaskModel.status == statusId)

        if taskId is not None:
            filter.append(TaskModel.id == taskId)

        if isUserAdmin is False:
            filter.append(TaskModel.clientOrgId.in_(
                TaskStorage.getOrganizationsIdByOperatorId(operatorId)))

        try:
            global session

            query = session.query(*queryFields)\
                .select_from(TaskModel)\
                .join(OrganizationModel, OrganizationModel.id == TaskModel.clientOrgId)\
                .join(ClientDeviceModel, ClientDeviceModel.deviceId == TaskModel.deviceId)\
                .join(DeviceModel, DeviceModel.id == ClientDeviceModel.deviceId)\
                .outerjoin(AstUserModel, AstUserModel.id == TaskModel.operatorId) \
                .filter(*filter)\

            if order == "asc":
                query = query.order_by(TaskModel.id.asc())

            elif order == "desc":
                query = query.order_by(TaskModel.id.desc())

            if limit is not None:
                query = query.limit(limit)

            return query.all()

        except OperationalError:
            session = AssistantDbContext().getSession()

        except DatabaseError as error:
            dbLog.exception(error)

    @staticmethod
    def getOrganizationsIdByOperatorId(id: int) -> List[int]:
        try:
            result = session.query(AstOrgUserModel.orgId) \
                .select_from(AstOrgUserModel) \
                .join(AstUserModel, AstUserModel.id == AstOrgUserModel.userId)\
                .filter(AstUserModel.id == id, AstUserModel.status == 0, AstOrgUserModel.status == 1)\
                .all()

            return [row.orgId for row in result]

        except DatabaseError as error:
            dbLog.exception(error)

    @staticmethod
    def getStatusLabel(id: int):
        statusList = {
            0: 'Новая',
            1: 'Принята в работу',
            2: 'Отработана',
            3: 'Отменена',
            4: 'Отклонена'
        }

        return statusList[id]
