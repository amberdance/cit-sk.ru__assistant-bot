from db.models.assistant import AstOrgUserModel, AstUserModel
from db.models.chat import ChatUserModel
from db.tables.assistant import AstUserTable
from db.tables.chat import ChatUserTable


print(AstUserTable.getAstUserModel(AstUserModel.id == 6795))
