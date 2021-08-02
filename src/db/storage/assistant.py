
from typing import Iterable, Union, List
from sqlalchemy.sql.expression import func
from sqlalchemy.exc import OperationalError
from ..context import AssistantDbContext
from ..storage.base import BaseStorage
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

        return session.query(*fields).select_from(OrganizationModel).join(AstOrgUserModel, AstUserModel).filter(*filter).all()

    @staticmethod
    def getAstUserModel(*filter: Iterable) -> Union[AstUserModel, List[AstUserModel]]:
        if(bool(filter) is False):
            raise Exception("Filter parameter is required")

        result = session.query(AstUserModel).filter(*filter).all()

        return result[0] if len(result) == 1 else result


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
    def getByFields(*fields: List, filter: Iterable = None, join: Iterable = None) -> List:
        query = session.query(*fields).select_from(TaskModel)

        if join is not None:
            query = query.outerjoin(*join)

        return [row._asdict() for row in query.filter(*filter).all()]

    @staticmethod
    def getModel(*filter: List, join: Iterable = None) -> Union[TaskModel, List[TaskModel]]:
        query = session.query(TaskModel)

        if join is not None:
            query = query.join(*join)

        result = query.filter(*filter).order_by(TaskModel.id.desc()).all()

        return result[0] if len(result) == 1 else result

    @staticmethod
    def getByOperatorId(operatorId: int, statusId: int = 0, isOperatorAdmin=False) -> List:
        global session

        queryFields = (
            TaskModel.id,
            TaskModel.descr,
            TaskModel.status,
            TaskModel.modDate.label('orderDate'),
            TaskModel.operatorOrgId.label('operatorOrgId'),
            DeviceModel.hid,
            ClientDeviceModel.title.label('client'),
            OrganizationModel.title.label("org"),
        )

        filter = [TaskModel.status == statusId]

        if isOperatorAdmin is False:
            filter.append(TaskModel.clientOrgId.in_(
                TaskStorage.getOrganizationsByOperatorId(operatorId)))

        try:
            return session.query(*queryFields)\
                .select_from(TaskModel)\
                .join(OrganizationModel, OrganizationModel.id == TaskModel.clientOrgId)\
                .join(ClientDeviceModel, ClientDeviceModel.deviceId == TaskModel.deviceId)\
                .join(DeviceModel, DeviceModel.id == ClientDeviceModel.deviceId)\
                .filter(*filter)\
                .order_by(TaskModel.id.asc())\
                .all()

        except OperationalError:
            session = AssistantDbContext().getSession()

    @staticmethod
    def getOrganizationsByOperatorId(id: int) -> List[int]:
        result = session.query(AstOrgUserModel.orgId) \
            .select_from(AstOrgUserModel) \
            .join(AstUserModel, AstUserModel.id == AstOrgUserModel.userId)\
            .filter(AstUserModel.id == id, AstUserModel.status == 0, AstOrgUserModel.status == 1)\
            .all()

        return [row.orgId for row in result]

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
