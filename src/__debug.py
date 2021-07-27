from db.models.assistant import TaskModel
from db.tables.assistant import TaskTable


print(len(TaskTable.getTaskFields(TaskModel.id, filter=[
      TaskModel.status == 0, TaskModel.operatorOrgId == 139])))
