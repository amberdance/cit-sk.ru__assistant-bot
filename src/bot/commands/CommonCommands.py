class CommonCommands:
    def initializeMessageHandler(bot):
        @bot.message_handler(commands=['help'])
        def helpCommand(message):
            bot.send_message(message.chat.id, "Это раздел помощь")
