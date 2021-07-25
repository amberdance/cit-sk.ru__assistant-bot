from config import IS_DEBUG_MODE, APP_PATH
import os
import logging


if __name__ == "__main__":

    logFile = f'{APP_PATH}/app.log'
    logLevel = logging.DEBUG if IS_DEBUG_MODE else logging.ERROR
    logger = logging.getLogger("Application")

    logging.getLogger("urllib3").setLevel(logging.ERROR)
    logging.basicConfig(handlers=[logging.FileHandler(logFile, "w")],
                        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                        datefmt='%Y/%m/%d %H:%M:%S',
                        level=logging.DEBUG)

    os.chmod(logFile, 0o777)

    logger.info("Application was started")

    if IS_DEBUG_MODE:
        from bot import PollingBot

        try:
            PollingBot(noneStopPolling=False, logLevel=logLevel)

        except (SystemExit, KeyboardInterrupt):
            logger.info("Application was terminated")

        except Exception as error:
            logger.exception(error)

    else:
        from bot import WebhookBot

        try:
            WebhookBot(botLoggingLevel=logLevel,
                       httpServerLoggingLevel=logLevel)

        except (SystemExit, KeyboardInterrupt):
            logger.info("Application was terminated")

        except Exception as error:
            logger.exception(error)
