from aiogram import types


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


def group_keyboard_common_inline(values_list: list):
    inline_keyboard = [types.InlineKeyboardButton(text=value, callback_data=value) for value in values_list]
    ikb = types.InlineKeyboardMarkup(resize_keyboard=True, inline_keyboard=[inline_keyboard])
    return ikb
