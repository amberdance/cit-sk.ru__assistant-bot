from typing import Any


def formatResultSetToDict(data) -> Any:
    result = []

    for row in data:
        print(row)
        # result.append(row.__dict__) if isinstance(
        #     row, object) else result.append(dict(row))
        result.append(dict(row))

    return result[0] if len(result) == 1 else result


# class MessageParser:

#     id = None
#     chatId = None
#     userId = None
#     isBot = False
#     def __init__(self, data) -> None:
#         print(data)
#         # self.chatId = data.message.chat.id
