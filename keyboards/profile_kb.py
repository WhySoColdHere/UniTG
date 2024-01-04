from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def profile_inline_keyboard(schedule_names: list):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for name in schedule_names:
        keyboard.add(InlineKeyboardButton(text=name, callback_data=f"PSN{name}"))

    return keyboard


def profile_actions_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text="Сделать основным", callback_data="profile_make_schedule_default"))
    keyboard.add(InlineKeyboardButton(text="Удалить", callback_data="profile_delete_schedule"))

    return keyboard
