from telebot import TeleBot
from db.context.DbContextBase import DbContextBase


class BaseController(DbContextBase):
    def __init__(self) -> None:
        super().__init__()
