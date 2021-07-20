from .DbBase import DbBase
from config import BOT_DB


class TelegramBotDatabase(DbBase):

    def __init__(self):
        super().__init__(host=BOT_DB['HOST'], login=BOT_DB['LOGIN'],
                         password=BOT_DB['PASSWORD'], db=BOT_DB['DB'])
