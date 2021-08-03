import logging
from aiohttp.web_app import Application
from aiohttp import web
import telebot
from config import BOT_TOKEN, WEBHOOK_URL_BASE, WEBHOOK_URL_PATH, WEBHOOK_LISTEN, WEBHOOK_LISTEN_PORT
from .controllers import CommonCommandsController, DatabaseCommandsController, ServiceCommandsController


class WebhookBot():

    __app: Application = web.Application()
    __bot: telebot.TeleBot = telebot.TeleBot(BOT_TOKEN)

    def __init__(self, botLoggingLevel: logging = logging.ERROR, httpServerLoggingLevel: logging = logging.ERROR) -> None:
        logging.basicConfig(level=httpServerLoggingLevel)
        telebot.logger.setLevel(botLoggingLevel)

        self.__bot.remove_webhook()
        self.__bot.set_webhook(WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)
        self.__app.router.add_post('/{token}/', self.__handle)

        controllers = (CommonCommandsController,
                       ServiceCommandsController,
                       DatabaseCommandsController,)

        for controller in controllers:
            controller(self.__bot).initialize()

        logging.getLogger('Application')
        logging.info("WebhookBot initialized")

        web.run_app(
            self.__app,
            host=WEBHOOK_LISTEN,
            port=WEBHOOK_LISTEN_PORT,
        )

    async def __handle(self, request) -> None:
        if request.match_info.get('token') != self.__bot.token:
            return web.Response(status=403)

        requestJSON = await request.json()

        self.__bot.process_new_updates(
            [telebot.types.Update.de_json(requestJSON)])

        return web.Response()
