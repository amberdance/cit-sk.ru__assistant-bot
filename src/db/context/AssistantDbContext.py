from .DbContextBase import DbContextBase
from config import ASSISTANT_DB


class AssistantDbContext(DbContextBase):

    def __init__(self) -> None:
        super().__init__(host=ASSISTANT_DB['HOST'], login=ASSISTANT_DB['LOGIN'],
                         password=ASSISTANT_DB['PASSWORD'], db=ASSISTANT_DB['DB'])
