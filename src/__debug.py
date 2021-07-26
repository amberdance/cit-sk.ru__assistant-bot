


from db.models.assistant import TaskModel
from db.tables.chat import ChatUserTable, ChatUserModel


subscribers = ChatUserTable.getUserFields(
                        ChatUserModel.astUserId, ChatUserModel.chatUserId, filter=[ChatUserModel.id ==9, ChatUserModel.isBlocked == False])
print(subscribers[0])
# print(Taskt.getTaskByChatUserId(1932081730))