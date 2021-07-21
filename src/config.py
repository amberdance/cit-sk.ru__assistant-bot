IS_DEBUG_MODE = True
TELEGRAMBOT_DB = {
    "DB": "telegrambot",
    "HOST": "127.0.0.1",
    "PORT": 5432,
    "LOGIN": "postgres",
    "PASSWORD": "",
}

ASSISTANT_DB = {
    "DB": "assistant",
    "HOST": "127.0.0.1",
    "PORT": 5432,
    "LOGIN": "postgres",
    "PASSWORD": "",
}

BOT_TOKEN = "1866567413:AAFBzR_uOkxlePU9ZbQl93gL1McWmFDoDAQ" if IS_DEBUG_MODE is True else "1926241792:AAHu4b3VeALdCbmTXy5V8D3N-n_va4d2fgU"
WEBHOOK_HOST = 'bot-ast.stavregion.ru'
WEBHOOK_LISTEN = '127.0.0.1'
WEBHOOK_PORT = 443
WEBHOOK_LISTEN_PORT = 8443
WEBHOOK_URL_BASE = f'https://{WEBHOOK_HOST}:{WEBHOOK_PORT}'
WEBHOOK_URL_PATH = f'/{BOT_TOKEN}/'
