from .DbContextBase import DbContextBase, TELEGRAMBOT_DB


class TelegramBotDbContext(DbContextBase):

    def __init__(self) -> None:
        super().getContext(host=TELEGRAMBOT_DB['HOST'], login=TELEGRAMBOT_DB['LOGIN'],
                           password=TELEGRAMBOT_DB['PASSWORD'], db=TELEGRAMBOT_DB['DB'])
