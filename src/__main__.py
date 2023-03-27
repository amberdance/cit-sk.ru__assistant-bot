import logging
from util import createLogger
from config import DEBUG_MODE
import bot


def setup():
    applicationLog = createLogger('Application', 'app.log')

    logLevel = logging.DEBUG if DEBUG_MODE else logging.ERROR
    loggers = ('pymorphy2.opencorpora_dict.wrapper',
               'aiohttp.access', 'asyncio', 'urllib3')

    for log in loggers:
        logging.getLogger(log).setLevel(logging.ERROR)

    try:
        if DEBUG_MODE:
            bot.PollingBot(noneStopPolling=False)

        else:
            createLogger('aiohttp.access', 'access.log')
            bot.WebhookBot(botLoggingLevel=logLevel,
                           httpServerLoggingLevel=logLevel)

    except Exception as error:
        applicationLog.exception(error)


if __name__ == "__main__":
    setup()
