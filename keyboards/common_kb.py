from aiogram import types


# Так как [_ for _ in cur.execute('SELECT * FROM Users')] --> [(...), (...) ...], то group_keyboard_db будем использовать
# с базой данных, а для автоматического формирования кнопок прибегнем к group_keyboard_common.
# def group_keyboard_db(values_list):
#     kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     for value_tuple in values_list:
#         kb.add(types.KeyboardButton(value_tuple[0]))
#     return kb

def group_keyboard_dict_reply(values_dict: dict):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for key in values_dict:
        kb.add(types.KeyboardButton(key))
    return kb


def group_keyboard_list_reply(names_list: list):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for value in names_list:
        kb.add(types.KeyboardButton(value))
    return kb

# Не уверен, будем ли мы использовать inline кнопки
# def group_keyboard_common_inline(values_list: dict):
#     inline_keyboard = [types.InlineKeyboardButton(text=value, callback_data=value) for value in values_list.keys()]
#     ikb = types.InlineKeyboardMarkup(resize_keyboard=True, inline_keyboard=[inline_keyboard])
#     return ikb
