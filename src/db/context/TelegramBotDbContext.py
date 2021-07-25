from .DbContextBase import DbContextBase, TELEGRAM_DB


class TelegramBotDbContext(DbContextBase):

    def __init__(self) -> None:
        super().getContext(host=TELEGRAM_DB['HOST'], login=TELEGRAM_DB['LOGIN'],
                           password=TELEGRAM_DB['PASSWORD'], db=TELEGRAM_DB['DB'])
