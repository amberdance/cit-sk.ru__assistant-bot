from .BaseTable import BaseTable
from ..models.TaskModel import TaskModel
from ..context.AssistantDbContext import AssistantDbContext

session = AssistantDbContext().getSession()


class TaskTable(BaseTable):

    @staticmethod
    def getTaskFields(*fields, filter: list = None) -> list:
        """Return dictionary data representaion"""

        return [row._asdict() for row in session.query(*fields).all()] if filter is None else [row._asdict() for row in session.query(*fields).filter(*filter).all()]

    @staticmethod
    def getTaskModel(*filter) -> TaskModel:
        """Return ORM model"""

        result = [row for row in session.query(TaskModel).all()] if filter is None else [
            row for row in session.query(TaskModel).filter(*filter).all()]

        return result[0] if len(result) == 1 else result

    @ staticmethod
    def addTask(user: TaskModel) -> TaskModel:
        BaseTable._insertRow(user, session=session)

        return user

    @staticmethod
    def upadteTask() -> None:
        BaseTable._updateRow(session)

    @staticmethod
    def deleteTask(user: TaskModel) -> None:
        BaseTable._deleteRow(user, session)
