from aiogram import types
from keyboards import common_kb, common_keyboard_names
from create_bot import bot, dp
from aiogram.dispatcher import FSMContext
from states.schedule_states import ScheduleStatesStudents
from states.get_online_states import OnlineStates
from states.client_schedule_states import ClientScheduleStates
from databases.online_database_dir.online_database import insert_into_online_db, get_online, DAYS_TO_STORE
from databases.client_schedule_database_dir.client_schedule_database import insert_into_client_db, get_client_schedule, \
    delete_client_schedule

DATA = []


@dp.message_handler(commands=['start'])
async def start_command_h(message: types.Message):
    insert_into_online_db(message.chat.id)

    await bot.send_message(message.chat.id, 'Здарова! Бот твоей шараги. Помощь по командам /help.')


@dp.message_handler(commands=['help'])
async def help_command_h(message: types.Message):
    insert_into_online_db(message.chat.id)

    await bot.send_message(message.chat.id, "You are loool.")


@dp.message_handler(commands=['get_id'])
async def get_id_h(message: types.Message):
    insert_into_online_db(message.chat.id)

    await bot.send_message(message.chat.id, f"id: {message.chat.id}.")


@dp.message_handler(commands=['get_online'], state='*')
async def get_online_command_h(message: types.Message, state: FSMContext):
    insert_into_online_db(message.chat.id)

    await bot.send_message(message.chat.id, 'Укажите период, за которой необходимо вывести статистику.')
    await state.set_state(OnlineStates.waiting_for_period.state)


@dp.message_handler(state=OnlineStates.waiting_for_period)
async def get_online_FSM_h(message: types.Message, state: FSMContext):
    online = get_online(message.text)
    if 0 < int(message.text) <= DAYS_TO_STORE:
        text = f"Онлайн за указанный период: {len(online)}."
    else:
        text = f"Мы храним информацию о пользователях не более чем {DAYS_TO_STORE} дней."

    await bot.send_message(message.chat.id, text)
    await state.finish()


####################################### ---> <Create_schedule>

@dp.message_handler(commands=['create_schedule'], state='*')
async def preparation_level_st_h(message: types.Message, state: FSMContext):
    insert_into_online_db(message.chat.id)
    await bot.send_message(message.chat.id, 'Выбери уровень подготовки.')
    await state.set_state(ScheduleStatesStudents.waiting_for_level_of_preparation.state)


@dp.message_handler(state=ScheduleStatesStudents.waiting_for_level_of_preparation)
async def institute_st_h(message: types.Message, state: FSMContext):
    DATA.append(message.text)

    await bot.send_message(message.chat.id, 'Выберите институт.')
    await state.set_state(ScheduleStatesStudents.waiting_for_institute.state)


@dp.message_handler(state=ScheduleStatesStudents.waiting_for_institute)
async def course_st_h(message: types.Message, state: FSMContext):
    DATA.append(message.text)

    await bot.send_message(message.chat.id, 'Выберите курс.')
    await state.set_state(ScheduleStatesStudents.waiting_for_course.state)


@dp.message_handler(state=ScheduleStatesStudents.waiting_for_course)
async def education_form_st_h(message: types.Message, state: FSMContext):
    DATA.append(message.text)

    await bot.send_message(message.chat.id, 'Выберите форму обучения.')
    await state.set_state(ScheduleStatesStudents.waiting_for_educational_form.state)


@dp.message_handler(state=ScheduleStatesStudents.waiting_for_educational_form)
async def group_st_h(message: types.Message, state: FSMContext):
    DATA.append(message.text)

    await bot.send_message(message.chat.id, 'Выберите группу.')
    await state.set_state(ScheduleStatesStudents.waiting_for_group.state)


@dp.message_handler(state=ScheduleStatesStudents.waiting_for_group)
async def schedule_name_st_h(message: types.Message, state: FSMContext):
    DATA.append(message.text)

    await bot.send_message(message.chat.id, 'Введите имя своего расписания.')
    await state.set_state(ScheduleStatesStudents.waiting_for_schedule_name.state)


@dp.message_handler(state=ScheduleStatesStudents.waiting_for_schedule_name)
async def adding_data_st_h(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, insert_into_client_db(message.chat.id, message.text, DATA),
                           reply_markup=types.ReplyKeyboardRemove())
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
@dp.message_handler(commands=['show_my_schedule'], state='*')
async def show_or_delete_client_schedule_h(message: types.Message, state: FSMContext):
    insert_into_online_db(message.chat.id)
    schedule = get_client_schedule(message.chat.id)

    if schedule is None:
        await bot.send_message(message.chat.id, "У вас нет ни одного расписания.")
        return

    async with state.proxy() as proxy_data:
        proxy_data['schedule'] = schedule

    await bot.send_message(message.chat.id, 'Выберите расписание.',
                           reply_markup=common_kb.group_keyboard_dict_reply(schedule))
    await state.set_state(ClientScheduleStates.waiting_for_schedule_to_show.state)


@dp.message_handler(state=ClientScheduleStates.waiting_for_schedule_to_show)
async def show_client_schedule_wait_for_schedule_h(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy_data:
        schedule = proxy_data['schedule']

    await bot.send_message(message.chat.id, schedule[message.text], reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


####################################### <Show_my_schedule\>


####################################### <Delete_my_schedule>
@dp.message_handler(commands=['delete_my_schedule'], state='*')
async def delete_client_schedule_h(message: types.Message, state: FSMContext):
    insert_into_online_db(message.chat.id)
    schedule = get_client_schedule(message.chat.id)
    if schedule is None:
        await bot.send_message(message.chat.id, schedule)
        return

    await bot.send_message(message.chat.id, 'Выберите расписание.',
                           reply_markup=common_kb.group_keyboard_dict_reply(schedule))
    await state.set_state(ClientScheduleStates.waiting_for_schedule_to_delete.state)


@dp.message_handler(state=ClientScheduleStates.waiting_for_schedule_to_delete)
async def delete_client_schedule_wait_for_schedule_h(message: types.Message, state: FSMContext):
    delete_client_schedule(message.chat.id, message.text)
    await bot.send_message(message.chat.id, "Расписание успешно удалено.", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()

####################################### <Delete_my_schedule\>
