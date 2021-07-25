import logging
from aiohttp.web_app import Application
from aiohttp import web
import telebot
from config import BOT_TOKEN, WEBHOOK_URL_BASE, WEBHOOK_URL_PATH, WEBHOOK_LISTEN, WEBHOOK_LISTEN_PORT
from controllers import CommonCommandsController, DatabaseCommandsController, ServiceCommandsController


class WebhookBot():

    __app: Application = web.Application()
    __telebot: telebot.TeleBot = telebot.TeleBot(BOT_TOKEN)

    def __init__(self, botLoggingLevel: logging = logging.ERROR, httpServerLoggingLevel: logging = logging.ERROR) -> None:

        logging.basicConfig(level=httpServerLoggingLevel)
        telebot.logger.setLevel(botLoggingLevel)

        self.__telebot.remove_webhook()
        self.__telebot.set_webhook(WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)

        self.__app.router.add_post('/{token}/', self.handle)
        self.initializeControllers()

        web.run_app(
            self.__app,
            host=WEBHOOK_LISTEN,
            port=WEBHOOK_LISTEN_PORT,
        )

    async def handle(self, request) -> None:
        if request.match_info.get('token') == self.__telebot.token:
            requestJSON = await request.json()
            self.__telebot.process_new_updates(
                [telebot.types.Update.de_json(requestJSON)])
            return web.Response()
        else:
            return web.Response(status=403)

    def initializeControllers(self) -> None:
        controllers = (CommonCommandsController,
                       ServiceCommandsController, DatabaseCommandsController)

        for obj in controllers:
            obj.initializeMessageHandler(self.__telebot)
