import logging
from config import DEBUG_MODE, BASE_DIR
import bot

if __name__ == "__main__":
    logFile = f'{BASE_DIR}/app.log'
    logLevel = logging.DEBUG if DEBUG_MODE else logging.ERROR
    logger = logging.getLogger("Application")
    loggers = ('pymorphy2.opencorpora_dict.wrapper',
               'asyncio', 'urllib3', 'aiohttp.access')

    for log in loggers:
        logging.getLogger(log).setLevel(logging.ERROR)

    logging.basicConfig(handlers=[logging.FileHandler(logFile, "a", encoding="utf-8")],
                        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                        datefmt='%Y/%m/%d %H:%M:%S',
                        level=logging.DEBUG)

    try:
        if DEBUG_MODE:
            bot.PollingBot(noneStopPolling=False)

        else:
            bot.WebhookBot(botLoggingLevel=logLevel,
                           httpServerLoggingLevel=logLevel)

    except Exception as error:
        logger.exception(error)
