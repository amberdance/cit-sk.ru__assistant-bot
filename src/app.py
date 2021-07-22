from config import IS_DEBUG_MODE


if __name__ == "__main__":

    if IS_DEBUG_MODE:
        from bot.PollingBot import PollingBot

        PollingBot()
    else:
        from bot.WebhookBot import WebhookBot
        import logging

        WebhookBot(botLoggingLevel=logging.DEBUG,
                   httpServerLoggingLevel=logging.DEBUG)
