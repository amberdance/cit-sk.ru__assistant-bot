from .DbBase import DbBase
from config import ASSISTANT_DB


class AssistantDb(DbBase):
    def __init__(self):
        super().__init__(host=ASSISTANT_DB['HOST'], login=ASSISTANT_DB['LOGIN'],
                         password=ASSISTANT_DB['PASSWORD'], db=ASSISTANT_DB['DB'])
