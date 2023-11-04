from aiogram import types

import keyboards.common_keyboard_names
from keyboards import common_kb
from create_bot import bot, dp, ADMINS_CHAT_ID

print("user_handlers")


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(message.chat.id, 'Здарова! Бот твоей шараги. Помощь по командам /help')


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await bot.send_message(message.chat.id, "You are loool")


@dp.message_handler(commands=['id'])  # type(message.chat.id) == int
async def get_group_id(message: types.Message):
    if message.chat.id == ADMINS_CHAT_ID:
        await bot.send_message(message.chat.id, "Admin chat")
    await bot.send_message(message.chat.id, f"{message.chat.id}: {type(message.chat.id)}")


@dp.message_handler(commands=['show_schedule'])
async def show_schedule(message: types.Message):
    await bot.send_message(message.chat.id, 'Выбери группу в которой учишься',
                           reply_markup=common_kb.group_keyboard_common(keyboards.common_keyboard_names.role_list()))
