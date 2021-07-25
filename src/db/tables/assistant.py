
from typing import Union
from db.tables.BaseTable import BaseTable
from ..models.assistant import TaskModel, AstOrgUserModel, AstUserModel, OrganizationModel
from ..context.AssistantDbContext import AssistantDbContext

session = AssistantDbContext().getSession()


class AstUserTable(BaseTable):
    @staticmethod
    def getOrganization(*filter: property) -> list:
        if(bool(filter) is False):
            raise Exception("Filter parameter is required")

        return session.query(OrganizationModel.id.label('orgId'), OrganizationModel.title, AstOrgUserModel.id, AstUserModel.id.label('userId'), AstUserModel.email,
                             AstUserModel.username).join(OrganizationModel, AstUserModel).filter(*filter).all()

    @staticmethod
    def getAstUserModel(*filter: property) -> Union[AstUserModel, list[AstUserModel]]:
        if(bool(filter) is False):
            raise Exception("Filter parameter is required")

        result = session.query(AstUserModel).filter(*filter).all()

        return result[0] if len(result) == 1 else result


class TaskTable(BaseTable):

    @staticmethod
    def getTaskFields(*fields: property, filter: list = [], join: list = None) -> list:
        """Return dictionary data representaion"""

        query = session.query(*fields)

        if join is not None:
            query = query.join(*join)

        result = [row._asdict() for row in query.filter(*filter).all()]

        return result[0] if len(result) == 1 else result

    @staticmethod
    def getTaskModel(*filter: property) -> TaskModel:
        """Return ORM model"""

        result = [row for row in session.query(
            TaskModel).filter(*filter).all()]

        return result[0] if len(result) == 1 else result

    @staticmethod
    def getTaskMeta(*filter: property) -> list:
        result = session.query(TaskModel.id,  TaskModel.orderDate, TaskModel.descr, TaskModel.status,
                               AstUserModel.username).join(AstUserModel).filter(*filter).all()

        return result[0] if len(result) == 1 else result

    @ staticmethod
    def getStatusLabel(id: int):
        statusList = ('Новая', 'Принята в работу',
                      'Отработана', 'Отменена', 'Отклонена')

        return statusList[id]

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
