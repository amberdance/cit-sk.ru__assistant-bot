from db.storage.assistant import TaskStorage


print(TaskStorage.getByOperatorId(2280, 0, isOperatorAdmin=True))