from db.models.assistant import TaskModel
from db.tables.assistant import TaskTable


print(TaskTable.getTaskModel(TaskModel.status == 1))