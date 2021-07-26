
import re
from typing import Union, List
from ..tables.BaseTable import BaseTable
from ..tables.chat import *
from ..models.assistant import *
from ..context import AssistantDbContext

session = AssistantDbContext().getSession()


class AstUserTable(BaseTable):
    @staticmethod
    def getOrganization(*filter: property) -> List:
        if(bool(filter) is False):
            raise Exception("Filter parameter is required")

        return session.query(OrganizationModel.id.label('orgId'), OrganizationModel.title, AstOrgUserModel.id, AstUserModel.id.label('userId'), AstUserModel.email,
                             AstUserModel.username).join(OrganizationModel, AstUserModel).filter(*filter).all()

    @staticmethod
    def getAstUserModel(*filter: property) -> Union[AstUserModel, List[AstUserModel]]:
        if(bool(filter) is False):
            raise Exception("Filter parameter is required")

        result = session.query(AstUserModel).filter(*filter).all()

        return result[0] if len(result) == 1 else result


class TaskTable(BaseTable):

    @staticmethod
    def getTaskFields(*fields: property, filter: List = [], join: List = None) -> List:
        query = session.query(*fields)

        if join is not None:
            query = query.join(*join)

        return [row._asdict() for row in query.filter(*filter).all()]

    @staticmethod
    def getTaskModel(*filter: property, join: List = None) -> Union[TaskModel, List[TaskModel]]:
        query = session.query(TaskModel)

        if join is not None:
            query = query.join(*join)

        result = query.filter(*filter).all()

        return result[0] if len(result) == 1 else result

    @staticmethod
    def getTaskByChatUserId(chatUserId: int, taskStatusId: int = 0) -> List:
        operatorId = ChatUserTable.getUserFields(ChatUserModel.astUserId, filter=[
            ChatUserModel.chatId == chatUserId])[0]['astUserId']

        return TaskTable.getTaskFields(TaskModel.id, TaskModel.descr, TaskModel.status, TaskModel.orderDate, OrganizationModel.title.label(
            "org"), filter=[TaskModel.status == taskStatusId, TaskModel.operatorId == operatorId], join=[OrganizationModel])

    @ staticmethod
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
