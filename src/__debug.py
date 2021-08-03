baseCommands = (
    "/reg - регистрация нового пользователя",
    "/userid - id пользователя",
    "/tasks - заявки",
    "/cancel - отмена текущей команды"
)

adminCommands = (
    "/subscribe - подписка на рассылку",
    "/unsubscribe - отписаться от рассылки",
    "/purgeusr - удалить заблокированных пользователей"
)

print("\n".join(baseCommands) + "\n".join(adminCommands))
