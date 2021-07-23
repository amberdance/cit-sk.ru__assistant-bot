
from .BaseTable import BaseTable
from ..models.assistant import TaskModel, AstOrgUserModel, AstUserModel, OrganizationModel
from ..context.AssistantDbContext import AssistantDbContext

session = AssistantDbContext().getSession()


class AstUserTable():
    @staticmethod
    def getOrganization(*filter: property) -> list:
        if(bool(filter) is False):
            raise Exception("Filter parameter is passed")

        return session.query(OrganizationModel.id, OrganizationModel.title, AstOrgUserModel.id, AstUserModel.id, AstUserModel.email,
                             AstUserModel.username).join(OrganizationModel, AstUserModel).filter(*filter).all()


class TaskTable():

    @staticmethod
    def getTaskFields(*fields: property, filter: list = None) -> list:
        """Return dictionary data representaion"""

        return [row._asdict() for row in session.query(*fields).all()] if filter is None else [row._asdict() for row in session.query(*fields).filter(*filter).all()]

    @staticmethod
    def getTaskModel(*filter: property) -> TaskModel:
        """Return ORM model"""

        result = [row for row in session.query(TaskModel).all()] if filter is None else [
            row for row in session.query(TaskModel).filter(*filter).all()]

        return result[0] if len(result) == 1 else result

    @ staticmethod
    def addTask(user: TaskModel) -> TaskModel:
        BaseTable.insertRow(user, session=session)

        return user

    @staticmethod
    def upadteTask() -> None:
        BaseTable.updateRow(session)

    @staticmethod
    def deleteTask(user: TaskModel) -> None:
        BaseTable.deleteRow(user, session)
