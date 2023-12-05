from aiogram import types
from keyboards import common_kb, common_keyboard_names
from create_bot import bot, dp
from aiogram.dispatcher import FSMContext
from states.schedule_states import ScheduleStatesStudents
from states.get_online_states import OnlineStates
from databases.online_database_dir.online_database import insert_into_online_db, get_online, DAYS_TO_STORE
from databases.client_schedule_database_dir.client_schedule_database import insert_into_client_db, get_client_schedule

# from databases.schedule_database_dir.rudn_database import get_schedule, select_notes

DATA = []


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(message.chat.id, 'Здарова! Бот твоей шараги. Помощь по командам /help.')
    insert_into_online_db(message.chat.id)


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await bot.send_message(message.chat.id, "You are loool.")
    insert_into_online_db(message.chat.id)


@dp.message_handler(commands=['get_id'])
async def get_id(message: types.Message):
    await bot.send_message(message.chat.id, f"id: {message.chat.id}.")
    insert_into_online_db(message.chat.id)


@dp.message_handler(commands=['get_online'], state='*')
async def get_online_command(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, 'Укажите период, за которой необходимо вывести статистику.')
    await state.set_state(OnlineStates.waiting_for_period.state)
    insert_into_online_db(message.chat.id)


@dp.message_handler(state=OnlineStates.waiting_for_period)
async def get_online_FSM(message: types.Message, state: FSMContext):
    if 0 < int(message.text) <= DAYS_TO_STORE:
        await bot.send_message(message.chat.id, f"Онлайн за указанный период: {get_online(message.text)}.")
    else:
        await bot.send_message(message.chat.id,
                               f"Мы храним информацию о пользователях не более чем {DAYS_TO_STORE} дней.")
    await state.finish()


####################################### ---> <Create_schedule>

@dp.message_handler(commands=['create_schedule'], state='*')
async def institute_schedule_st(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, 'Выбери уровень подготовки.')
    await state.set_state(ScheduleStatesStudents.waiting_for_level_of_preparation.state)
    insert_into_online_db(message.chat.id)


@dp.message_handler(state=ScheduleStatesStudents.waiting_for_level_of_preparation)
async def course_schedule_st(message: types.Message, state: FSMContext):
    await state.update_data(level_of_preparation_st=message.text)
    DATA.append(message.text)

    await bot.send_message(message.chat.id, 'Выберите институт.')
    await state.set_state(ScheduleStatesStudents.waiting_for_institute.state)


@dp.message_handler(state=ScheduleStatesStudents.waiting_for_institute)
async def education_form_schedule_st(message: types.Message, state: FSMContext):
    await state.update_data(course_st=message.text)
    DATA.append(message.text)

    await bot.send_message(message.chat.id, 'Выберите курс.')
    await state.set_state(ScheduleStatesStudents.waiting_for_course.state)


@dp.message_handler(state=ScheduleStatesStudents.waiting_for_course)
async def group_schedule_st(message: types.Message, state: FSMContext):
    await state.update_data(educational_form_st=message.text)
    DATA.append(message.text)

    await bot.send_message(message.chat.id, 'Выберите форму обучения.')
    await state.set_state(ScheduleStatesStudents.waiting_for_educational_form.state)


@dp.message_handler(state=ScheduleStatesStudents.waiting_for_educational_form)
async def final_schedule_st(message: types.Message, state: FSMContext):
    await state.update_data(group_st=message.text)
    DATA.append(message.text)

    await bot.send_message(message.chat.id, 'Выберите группу.')
    await state.set_state(ScheduleStatesStudents.waiting_for_group.state)


@dp.message_handler(state=ScheduleStatesStudents.waiting_for_group)
async def final_schedule_st(message: types.Message, state: FSMContext):
    await state.update_data(group_st=message.text)
    DATA.append(message.text)

    insert_into_client_db(message.chat.id, DATA)
    await bot.send_message(message.chat.id, DATA)
    await state.finish()


# Валидатор
# async def kinda_validator_st(message, elems, err_message):
#     if message.text not in elems:
#         await bot.send_message(message.chat.id, err_message)
#         return

# Пример использования валидатора. Пока что не будем с ним сношаться.
# await kinda_validator_st(message, common_keyboard_names.levels_of_preparation(),
#                          "Выберите существующий уровень подготовки!")

# Пример использования добавления клавиатуры.
# await bot.send_message(message.chat.id, 'Выберите форму обучения.',
#                        reply_markup=common_kb.group_keyboard_common_reply(
#                            common_keyboard_names.education_forms()))

####################################### <Create_schedule\>

####################################### <Show_my_schedule>
@dp.message_handler(commands=['show_my_schedule'])
async def show_client_schedule(message: types.Message):
    await bot.send_message(message.chat.id, get_client_schedule(message.chat.id))
    insert_into_online_db(message.chat.id)

####################################### <Show_my_schedule>
