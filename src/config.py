import os

DEBUG_MODE = True
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOT_TOKEN = "5716696682:AAF0UsuSJ-N8zHinTOMX4mSPCF-gak_r5GY" if DEBUG_MODE is True else "1926241792:AAHu4b3VeALdCbmTXy5V8D3N-n_va4d2fgU"
WEBHOOK_HOST = 'bot-ast.stavregion.ru'
WEBHOOK_LISTEN = '127.0.0.1'
WEBHOOK_PORT = 443
WEBHOOK_LISTEN_PORT = 8443
WEBHOOK_URL_BASE = f'https://{WEBHOOK_HOST}:{WEBHOOK_PORT}'
WEBHOOK_URL_PATH = f'/{BOT_TOKEN}/'

TELEGRAM_DB = {
    "DB": "telegram_db",
    "HOST": "127.0.0.1",
    "PORT": 5432,
    "LOGIN": "root",
    "PASSWORD": "root",
}

ASSISTANT_DB = {
    "DB": "assistant_db",
    "HOST": "127.0.0.1",
    "PORT": 5432,
    "LOGIN": "root",
    "PASSWORD": "root",
}
