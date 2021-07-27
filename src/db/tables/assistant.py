
import re
import logging
from typing import Iterable, Union, List
from sqlalchemy.sql.expression import func
from sqlalchemy.exc import OperationalError
from ..tables.BaseTable import BaseTable
from ..tables.chat import *
from ..models.assistant import *
from ..context import AssistantDbContext

session = AssistantDbContext().getSession()


class AstUserTable(BaseTable):
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


class TaskTable(BaseTable):

    @staticmethod
    def getTaskFields(*fields: List, filter: Iterable = None, join: Iterable = None) -> List:
        query = session.query(*fields).select_from(TaskModel)

        if join is not None:
            query = query.outerjoin(*join)

        return [row._asdict() for row in query.filter(*filter).all()]

    @staticmethod
    def getTaskModel(*filter: List, join: Iterable = None) -> Union[TaskModel, List[TaskModel]]:
        query = session.query(TaskModel)

        if join is not None:
            query = query.join(*join)

        result = query.filter(*filter).all()

        return result[0] if len(result) == 1 else result

    @staticmethod
    def getTaskByChatUserId(chatUserId: int, statusId: int = 0) -> List:

        global session

        operatorId = ChatUserTable.getUserFields(ChatUserModel.astUserId, filter=[
            ChatUserModel.chatId == chatUserId])['astUserId']

        queryFields = (
            TaskModel.id,
            TaskModel.descr,
            TaskModel.status,
            func.to_char(TaskModel.orderDate,
                         "dd.mm.YYYY HH:ss:mm").label('orderDate'),
            DeviceModel.hid,
            TaskModel.operatorOrgId.label('operatorOrgId'),
            ClientDeviceModel.title.label('clientTitle'),
            OrganizationModel.title.label("orgTitle"),
        )

        filter = (
            TaskModel.status == statusId,
            TaskModel.operatorId == operatorId
        )

        try:
            return session.query(*queryFields) \
                .select_from(TaskModel) \
                .join(OrganizationModel, OrganizationModel.id == TaskModel.clientOrgId) \
                .join(ClientDeviceModel, ClientDeviceModel.deviceId == TaskModel.deviceId) \
                .join(DeviceModel, DeviceModel.id == ClientDeviceModel.deviceId) \
                .join(AstUserModel, AstUserModel.id == TaskModel.operatorId) \
                .filter(*filter).all()

        except OperationalError:
            logging.getLogger('Application').exception(
                'Server closed the connection')

            session = AssistantDbContext().getSession()

            logging.getLogger('Application').info('Reconnected to server')

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

    @ staticmethod
    def getStatusId(key: str):
        idList = {
            'Новая': 0,
            'Принята в работу': 1,
            'Отработана': 2,
            'Отменена': 3,
            'Отклонена': 4
        }

        matchedKey = [k for k in idList.keys() if re.findall(
            f"{key}+.*", k, re.IGNORECASE)]

        return idList[matchedKey[0]] if bool(matchedKey) else idList[0]

    @ staticmethod
    def addTask(user: TaskModel) -> TaskModel:
        BaseTable.insertRow(user, session=session)

        return user

    @ staticmethod
    def upadteTask() -> None:
        BaseTable.updateRow(session)

    @ staticmethod
    def deleteTask(user: TaskModel) -> None:
        BaseTable.deleteRow(user, session)
