from db.tables.chat import ChatUserTable, ChatUserModel


print(ChatUserTable.getUserFields(ChatUserModel.astUserId, filter=[
            ChatUserModel.chatId == chatUserId])[0]['astUserId'])