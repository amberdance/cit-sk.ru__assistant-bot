from db.tables.assistant import TaskTable
from db.tables.chat import ChatUserTable, ChatUserModel


subscribers = ChatUserTable.getUserFields(
    ChatUserModel.chatUserId, filter=[ChatUserModel.isBlocked == False])

print("test" in {"test1":1})