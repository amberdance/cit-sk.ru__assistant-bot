# Only for usage in public network

import logging
import re
from aiohttp.web_app import Application
from config import BOT_TOKEN, WEBHOOK_LISTEN, WEBHOOK_LISTEN_PORT
from aiohttp import web
import telebot
from bot.controllers.CommonCommandsController import CommonCommandsController
from bot.controllers.DatabaseCommandsController import DatabaseCommandsController
from bot.controllers.ServiceCommandsController import ServiceCommandsController


class WebhookBot(CommonCommandsController, DatabaseCommandsController, ServiceCommandsController):

    __app: Application = web.Application()
    __telebot: telebot.TeleBot = telebot.TeleBot(BOT_TOKEN)

    def __init__(self, botLoggingLevel: logging = logging.INFO, httpServerLoggingLevel: logging = logging.INFO) -> None:

        logging.basicConfig(level=botLoggingLevel)
        telebot.logger.setLevel(httpServerLoggingLevel)

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
        controllersList = WebhookBot.mro()

        for controller in controllersList:
            if re.findall(r"Controller", controller.__name__):
                controller.initializeMessageHandler(self.__telebot)
