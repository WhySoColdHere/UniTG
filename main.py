import telebot as tb
from token_file import token
from commands import commands_list, commands_list_txt

bot = tb.TeleBot(token)


# Обработчик команды /about_us --> кидает ссылки на наш GitHub
@bot.message_handler(commands=commands_list[0])
def command_credits(mess):
    bot.send_message(mess.chat.id,
                     "Ссылки на GitHub разработчиков:\nhttps://github.com/WhySoColdHere\nhttps://github.com/Retol17")


# Обработчик команды /help --> Возвращает список команд
@bot.message_handler(commands=commands_list[1])
def command_help(mess):
    bot.send_message(mess.chat.id, commands_list_txt)


@bot.message_handler()
def unknown_command(mess):
    bot.send_message(mess.chat.id, "Хз о чем ты, ковыляй отсюда")


bot.polling(none_stop=True)
