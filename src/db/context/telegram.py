from .base import DbContextBase
from config import TELEGRAM_DB


class TelegramBotDbContext(DbContextBase):

    def __init__(self) -> None:
        super().__init__(host=TELEGRAM_DB['HOST'], login=TELEGRAM_DB['LOGIN'],
                           password=TELEGRAM_DB['PASSWORD'], db=TELEGRAM_DB['DB'])
