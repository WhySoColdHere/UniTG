from aiogram import types


# Так как [_ for _ in cur.execute('SELECT * FROM Users')] --> [(...), (...) ...] то group_keyboard_db будем использовать
# с базой данных, а для автоматического формирования кнопок прибегнем к group_keyboard_common.
def group_keyboard_db(values_list):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for value_tuple in values_list:
        but = types.KeyboardButton(value_tuple[0])
        kb.add(but)
    return kb


def group_keyboard_common(values_list):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for value in values_list:
        but = types.KeyboardButton(value)
        kb.add(but)
    return kb
