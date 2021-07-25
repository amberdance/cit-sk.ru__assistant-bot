from config import IS_DEBUG_MODE, APP_PATH
import logging


if __name__ == "__main__":
    logLevel = logging.DEBUG if IS_DEBUG_MODE else logging.ERROR
    logger = logging.getLogger("Application")

    logging.getLogger("urllib3").setLevel(logging.ERROR)
    logging.basicConfig(filename=f'{APP_PATH}/app.log',
                        filemode='a',
                        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                        datefmt='%Y/%m/%d %H:%M:%S',
                        level=logLevel)

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
        import logging

        try:
            WebhookBot(botLoggingLevel=logLevel,
                       httpServerLoggingLevel=logging.DEBUG)

        except (SystemExit, KeyboardInterrupt):
            logger.info("Application was terminated")

        except Exception as error:
            logger.exception(error)
