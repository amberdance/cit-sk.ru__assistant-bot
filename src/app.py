import logging
from util import createLogger
from config import DEBUG_MODE
import bot


if __name__ == "__main__":
    applicationLog = createLogger('Application', 'app.log')
    accessLog = createLogger('aiohttp.access', 'access.log')
    logLevel = logging.DEBUG if DEBUG_MODE else logging.ERROR
    loggers = ('pymorphy2.opencorpora_dict.wrapper', 'asyncio', 'urllib3')

    for log in loggers:
        logging.getLogger(log).setLevel(logging.ERROR)

    try:
        if DEBUG_MODE:
            bot.PollingBot(noneStopPolling=False)

        else:
            bot.WebhookBot(botLoggingLevel=logLevel,
                           httpServerLoggingLevel=logLevel)

    except Exception as error:
        applicationLog.exception(error)
