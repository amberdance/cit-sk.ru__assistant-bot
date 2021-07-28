from db.tables.assistant import TaskTable
from db.tables.chat import ChatUserTable, ChatUserModel


subscribers = ChatUserTable.getUserFields(
    ChatUserModel.chatUserId, filter=[ChatUserModel.isBlocked == False])


for user in subscribers:
    # chatId = user[0]['chatUserId']
    
    print(user)