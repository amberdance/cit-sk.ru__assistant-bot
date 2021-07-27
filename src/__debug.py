from db.tables.assistant import TaskTable
from db.tables.chat import ChatUserTable, ChatUserModel


# print(TaskTable.getTaskByChatUserId(686739701))

print((ChatUserTable.getUserFields(ChatUserModel.chatUserId, filter=[
                                                              ChatUserModel.isBlocked == False]),))