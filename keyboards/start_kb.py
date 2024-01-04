from aiogram import types


def group_keyboard_list_reply(names_list: list):
    kb = list()

    kb.append([
        types.KeyboardButton(text="Сегодня"),
        types.KeyboardButton(text="Завтра")
    ])

    if names_list is not None:
        for schedule_name in names_list:
            kb.append([schedule_name])

    kb.append([
        types.KeyboardButton(text="Справка"),
        types.KeyboardButton(text="Профиль")
    ])

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )

    return keyboard
