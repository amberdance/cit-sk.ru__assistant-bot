from .DbContextBase import DbContextBase
from config import TELEGRAMBOT_DB


class TelegramBotDbContext(DbContextBase):

    def __init__(self) -> None:
        super().__init__(host=TELEGRAMBOT_DB['HOST'], login=TELEGRAMBOT_DB['LOGIN'],
                         password=TELEGRAMBOT_DB['PASSWORD'], db=TELEGRAMBOT_DB['DB'])
