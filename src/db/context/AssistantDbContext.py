from .DbContextBase import DbContextBase, ASSISTANT_DB


class AssistantDbContext(DbContextBase):

    def __init__(self) -> None:
        super().getContext(host=ASSISTANT_DB['HOST'], login=ASSISTANT_DB['LOGIN'],
                           password=ASSISTANT_DB['PASSWORD'], db=ASSISTANT_DB['DB'])
