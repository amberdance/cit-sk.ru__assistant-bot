test = ({"Помощь": "/help\n/userid"}, {"Работа с заявками": ("/task")})
htmlTemplate = "Ты можешь управлять взаимодействовать со мной с помощью следующих команд:"

for i, item in enumerate(test):
    for key in test[i].keys():
        htmlTemplate += f"\n{key}:\n"
        value = item[key]
        htmlTemplate += f"\n{value}\n"


print(htmlTemplate)
