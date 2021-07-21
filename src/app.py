from config import IS_DEBUG_MODE
from db.tables.UserTable import UserModel, UserTable

if __name__ == "__main__":
    UserTable.addUser(UserModel(astUserId=1, role=1, chatUserId=1))
    # if IS_DEBUG_MODE:
    #     from bot.PollingBot import PollingBot

    #     PollingBot()
    # else:
    #     from bot.WebhookBot import WebhookBot
    #     import logging

    #     WebhookBot(botLoggingLevel=logging.DEBUG,
    #                httpServerLoggingLevel=logging.DEBUG)
