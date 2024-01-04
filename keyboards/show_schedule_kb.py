from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def show_schedule_inline_week_days_kb(days_of_week: list):
    kb_upper = [InlineKeyboardButton(text=day, callback_data=f"upper_week{day}") for day in days_of_week]
    kb_lower = [InlineKeyboardButton(text=day, callback_data=f"lower_week{day}") for day in days_of_week]

    keyboard = InlineKeyboardMarkup(inline_keyboard=[kb_upper, kb_lower])
    return keyboard
