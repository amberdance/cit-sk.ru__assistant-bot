from db.tables.ChatUserTable import ChatUserModel, ChatUserTable

print(ChatUserTable.addUser(ChatUserModel(astUserId=1, role=1, chatUserId=1)).id)
