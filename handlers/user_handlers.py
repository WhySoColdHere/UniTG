from aiogram import types
from keyboards import common_kb, common_keyboard_names
from create_bot import bot, dp
from aiogram.dispatcher import FSMContext
from states.schedule_states import ScheduleStatesStudents
from states.get_online_states import OnlineStates
from states.client_schedule_states import ClientScheduleStates
from databases.schedule_database_dir.rudn_database import get_institutes_names, get_courses_names, \
    get_education_forms_names, get_groups_names, get_client_schedule_from_rudn
from databases.online_database_dir.online_database import insert_into_online_db, get_online, DAYS_TO_STORE
from databases.client_schedule_database_dir.client_schedule_database import insert_into_client_db, \
    get_client_schedule_names, get_client_schedule_week_days, delete_client_schedule, DAYS_OF_WEEK

DATA_DICT = dict()


@dp.message_handler(commands=['start'])
async def start_command_h(message: types.Message):
    insert_into_online_db(message.chat.id)
    await help_command_h(message)
    # await bot.send_message(message.chat.id, 'Здарова! Бот твоей шараги. Помощь по командам /help.')


@dp.message_handler(commands=['help'])
async def help_command_h(message: types.Message):
    insert_into_online_db(message.chat.id)

    await bot.send_message(message.chat.id, "You are loool.")


@dp.message_handler(commands=['get_id'])
async def get_id_h(message: types.Message):
    insert_into_online_db(message.chat.id)
    await bot.send_message(message.chat.id, f"id: {message.chat.id}.")


@dp.message_handler(commands=['break'], state='*')
async def get_online_command_h(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.chat.id, "Введите желаемую команду.")


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


####################################### <Create_schedule>

@dp.message_handler(commands=['create_schedule'], state='*')
async def preparation_level_st_h(message: types.Message, state: FSMContext):
    insert_into_online_db(message.chat.id)

    await bot.send_message(message.chat.id, 'Выбери уровень подготовки.',
                           reply_markup=common_kb.group_keyboard_list_reply(
                               common_keyboard_names.levels_of_preparation()))
    await state.set_state(ScheduleStatesStudents.waiting_for_level_of_preparation.state)


@dp.message_handler(state=ScheduleStatesStudents.waiting_for_level_of_preparation)
async def institute_st_h(message: types.Message, state: FSMContext):
    institute_rudn_data = get_institutes_names(message.text)
    DATA_DICT["preparation_node_id"] = institute_rudn_data["preparation_node_id"]

    await bot.send_message(message.chat.id, 'Выберите институт.',
                           reply_markup=common_kb.group_keyboard_list_reply(institute_rudn_data["names"]))

    await state.set_state(ScheduleStatesStudents.waiting_for_institute.state)


@dp.message_handler(state=ScheduleStatesStudents.waiting_for_institute)
async def course_st_h(message: types.Message, state: FSMContext):
    course_rudn_data = get_courses_names(message.text, DATA_DICT)
    DATA_DICT["institute_node_id"] = course_rudn_data["institute_node_id"]

    # await bot.send_message(message.chat.id, 'Выберите курс.')
    await bot.send_message(message.chat.id, 'Выберите курс.',
                           reply_markup=common_kb.group_keyboard_list_reply(course_rudn_data["names"]))
    await state.set_state(ScheduleStatesStudents.waiting_for_course.state)


@dp.message_handler(state=ScheduleStatesStudents.waiting_for_course)
async def education_form_st_h(message: types.Message, state: FSMContext):
    education_form_rudn_data = get_education_forms_names(message.text, DATA_DICT)
    DATA_DICT["course_node_id"] = education_form_rudn_data["course_node_id"]

    await bot.send_message(message.chat.id, 'Выберите форму обучения.',
                           reply_markup=common_kb.group_keyboard_list_reply(education_form_rudn_data["names"]))
    await state.set_state(ScheduleStatesStudents.waiting_for_educational_form.state)


@dp.message_handler(state=ScheduleStatesStudents.waiting_for_educational_form)
async def group_st_h(message: types.Message, state: FSMContext):
    group_rudn_data = get_groups_names(message.text, DATA_DICT)
    DATA_DICT["education_form_node_id"] = group_rudn_data["education_form_node_id"]

    await bot.send_message(message.chat.id, 'Выберите группу.',
                           reply_markup=common_kb.group_keyboard_list_reply(group_rudn_data["names"]))
    await state.set_state(ScheduleStatesStudents.waiting_for_group.state)


@dp.message_handler(state=ScheduleStatesStudents.waiting_for_group)
async def schedule_name_st_h(message: types.Message, state: FSMContext):
    DATA_DICT["group_name"] = message.text

    await bot.send_message(message.chat.id, 'Придумайте название своему расписанию.')
    await state.set_state(ScheduleStatesStudents.waiting_for_schedule_name.state)


@dp.message_handler(state=ScheduleStatesStudents.waiting_for_schedule_name)
async def adding_data_st_h(message: types.Message, state: FSMContext):
    data_dict_values = list(DATA_DICT.values())

    await bot.send_message(message.chat.id, insert_into_client_db(message.chat.id, message.text, data_dict_values),
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
async def show_client_schedule_h(message: types.Message, state: FSMContext):
    try:
        insert_into_online_db(message.chat.id)
        schedule = get_client_schedule_names(message.chat.id)

        if schedule is None:
            await bot.send_message(message.chat.id, "У вас нет ни одного расписания.")
            return

        async with state.proxy() as proxy_data:
            proxy_data['schedule'] = schedule
        # get_client_schedule(...) не распространяется дальше этой функции
        await bot.send_message(message.chat.id, 'Выберите расписание.',
                               reply_markup=common_kb.group_keyboard_dict_reply(schedule))
        await state.set_state(ClientScheduleStates.waiting_for_schedule_to_show.state)
    except Exception:
        await bot.send_message("Чет пошло не так, пробуй еще раз.")
        await state.finish()


@dp.message_handler(state=ClientScheduleStates.waiting_for_schedule_to_show)
async def show_client_schedule_wait_for_schedule_h(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as proxy_data:
            schedule = proxy_data['schedule']
            main_schedule = get_client_schedule_week_days(schedule[message.text])
            proxy_data['schedule'] = main_schedule['schedule']

        await bot.send_message(message.chat.id,
                               f"Выберите день недели.\nРасписание группы {main_schedule['schedule']['group_name']}.",
                               reply_markup=common_kb.group_keyboard_list_reply(DAYS_OF_WEEK))
        await state.set_state(ClientScheduleStates.waiting_for_day_of_week.state)

        # schedule[message.text] попадает в некую функцию, где подвергается обработке и возвращает расписание
        # на четную и нечетную неделю в виде инлайн кнопок (как в боте от Антона)
    except KeyError:
        await bot.send_message(message.chat.id, "Произошла ошибка KeyError, попробуйте снова.",
                               reply_markup=types.ReplyKeyboardRemove())
        await state.finish()


@dp.message_handler(state=ClientScheduleStates.waiting_for_day_of_week)
async def show_client_schedule_wait_for_schedule_h(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, "Умничка :)", reply_markup=types.ReplyKeyboardRemove())
    async with state.proxy() as proxy_data:
        schedule = proxy_data['schedule']

    await bot.send_message(message.chat.id, get_client_schedule_from_rudn(schedule, message.text))
    await state.finish()


####################################### <Show_my_schedule\>


####################################### <Delete_my_schedule>
@dp.message_handler(commands=['delete_my_schedule'], state='*')
async def delete_client_schedule_h(message: types.Message, state: FSMContext):
    insert_into_online_db(message.chat.id)
    schedule = get_client_schedule_names(message.chat.id)
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
