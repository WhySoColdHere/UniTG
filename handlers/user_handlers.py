from aiogram.dispatcher.filters import Text
from aiogram import types
from keyboards import common_kb, start_kb, profile_kb, show_schedule_kb
from create_bot import bot, dp
from aiogram.dispatcher import FSMContext
from states.start_command_states import StartCommandStates
from states.schedule_states import ScheduleStatesStudents
from states.get_online_states import OnlineStates
from states.client_schedule_states import ClientScheduleStates
from databases.schedule_database_dir.rudn_database import get_institutes_names, get_courses_names, \
    get_education_forms_names, get_groups_names, get_client_schedule_from_rudn
from databases.online_database_dir.online_database import insert_into_online_db, get_online, DAYS_TO_STORE
from databases.client_schedule_database_dir.client_schedule_database import insert_into_client_db, \
    get_client_schedule_names, get_client_schedule_dict, delete_client_schedule, DAYS_OF_WEEK, \
    get_default_client_schedule, make_client_schedule_default

DATA_DICT = dict()


@dp.message_handler(commands=['start'], state='*')
async def start_command_h(message: types.Message, state: FSMContext):
    insert_into_online_db(message.chat.id)

    start_schedules_list = get_client_schedule_names(message.chat.id)

    async with state.proxy() as proxy_data:
        proxy_data['start_schedules_list'] = start_schedules_list

    await bot.send_message(message.chat.id,
                           'Здравствуй, это бот с расписанием университета РУДН.\nВыбери желаемое действие',
                           reply_markup=start_kb.group_keyboard_list_reply(start_schedules_list))
    await state.set_state(StartCommandStates.waiting_for_button_click.state)


@dp.message_handler(state=StartCommandStates.waiting_for_button_click)
async def start_command_s(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy_data:
        start_schedules_list = proxy_data['start_schedules_list']
    default_buttons_names = ["Сегодня", "Завтра", "Справка", "Профиль"]

    if start_schedules_list is None:
        start_schedules_list = list()

    if (message.text not in start_schedules_list) and (message.text not in default_buttons_names):
        await bot.send_message(message.chat.id,
                               "Вы ввели некорректное в данном контексте сообщение, вызовите команду заново.")
        await state.finish()
        return

    if message.text == default_buttons_names[0]:
        pass
        await state.finish()

    elif message.text == default_buttons_names[1]:
        pass
        await state.finish()

    elif message.text == default_buttons_names[-2]:
        await bot.send_message(message.chat.id, "Здесь будет справка(?)")
        await state.finish()

    elif message.text == default_buttons_names[-1]:
        await profile_command(message)
        await state.finish()

    else:
        await state.set_state(ClientScheduleStates.waiting_for_schedule_to_show.state)
        await show_client_schedule_wait_for_schedule_h(message=message, state=state)


@dp.message_handler(state=ClientScheduleStates.waiting_for_schedule_to_show)
async def show_client_schedule_wait_for_schedule_h(message: types.Message, state: FSMContext):
    keyboard = show_schedule_kb.show_schedule_inline_week_days_kb(DAYS_OF_WEEK)

    async with state.proxy() as proxy_data:
        schedule = get_client_schedule_names(message.chat.id)  # {name: schedule, name: schedule...}
        main_schedule = get_client_schedule_dict(schedule[message.text])  # Добавляет ключи
        proxy_data['schedule'] = main_schedule['schedule']  # {'telegram_id': '1947491258', 'schedule_name': 'jhslj', }
        proxy_data['keyboard'] = keyboard

    await bot.send_message(message.chat.id,
                           f"Выберите день недели.\nРасписание группы {main_schedule['schedule']['group_name']}.",
                           reply_markup=keyboard)
    await state.set_state(ClientScheduleStates.waiting_for_day_of_week.state)


@dp.callback_query_handler(Text(startswith="upper_week"), state=ClientScheduleStates.waiting_for_day_of_week)
async def show_schedule_upper_week_callback_handler(callback: types.CallbackQuery, state: FSMContext):
    callback_data = callback.data[10:]
    async with state.proxy() as proxy_data:
        schedule = proxy_data['schedule']
        keyboard = proxy_data['keyboard']

    schedule = get_client_schedule_from_rudn(schedule, callback_data)['upper_week']

    await callback.message.edit_text(text=week_schedule(schedule, "Верхняя неделя"))
    await callback.message.edit_reply_markup(reply_markup=keyboard)


@dp.callback_query_handler(Text(startswith="lower_week"), state=ClientScheduleStates.waiting_for_day_of_week)
async def show_schedule_lover_week_callback_handler(callback: types.CallbackQuery, state: FSMContext):
    callback_data = callback.data[10:]
    async with state.proxy() as proxy_data:
        schedule = proxy_data['schedule']
        keyboard = proxy_data['keyboard']

    schedule = get_client_schedule_from_rudn(schedule, callback_data)['lower_week']

    await callback.message.edit_text(text=week_schedule(schedule, "Нижняя неделя"))
    await callback.message.edit_reply_markup(reply_markup=keyboard)


def week_schedule(schedule, week_pos):
    week_schedule_str = week_pos
    if is_schedule_empty(schedule):
        week_schedule_str += "Пар нет, урааа!"
    else:
        for lesson in schedule:
            week_schedule_str += f"\n\n{lesson['lesson_number']} пара({lesson['time']})\n{lesson['name']}({lesson['lesson_type']})" \
                                 f"\n{lesson['teacher']}\n{lesson['office']}\n\n\n"
    return week_schedule_str


def is_schedule_empty(schedule: list):
    if len(schedule) > 0:
        return False
    return True


@dp.message_handler(commands=['profile'])
async def profile_command(message: types.Message):
    insert_into_online_db(message.chat.id)

    schedule_names = get_client_schedule_names(message.chat.id)

    if schedule_names is None:
        await bot.send_message(message.chat.id, "У вас нет ни одного расписания.")
        return

    await bot.send_message(message.chat.id,
                           f"Telegram ID: {message.chat.id}\n\nВыберите расписание из списка для управления.",
                           reply_markup=profile_kb.profile_inline_keyboard(schedule_names))


@dp.callback_query_handler(Text(startswith="PSN"), state='*')
async def profile_callback_query(callback: types.CallbackQuery, state: FSMContext):
    callback_data = callback.data[3:]

    async with state.proxy() as proxy_data:
        proxy_data['profile_schedule_name'] = callback_data

    is_default_bool = "Да" if get_default_client_schedule(callback.from_user.id) == callback_data else "Нет"

    await callback.message.edit_text(text=f"Расписание {callback_data}\nОсновное: {is_default_bool}")
    await callback.message.edit_reply_markup(reply_markup=profile_kb.profile_actions_keyboard())


@dp.callback_query_handler(text="profile_make_schedule_default")
async def profile_callback_query_make_sch_def(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as proxy_data:
        profile_schedule_name = proxy_data['profile_schedule_name']

    result = make_client_schedule_default(callback.from_user.id, profile_schedule_name)
    answer = "Расписание стало основным." if result else "Что-то пошло не так, попробуйте ещё раз."
    await bot.send_message(callback.from_user.id, answer)


@dp.callback_query_handler(text="profile_delete_schedule")
async def profile_callback_query_del_sch(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as proxy_data:
        profile_schedule_name = proxy_data['profile_schedule_name']

    delete_client_schedule(callback.from_user.id, profile_schedule_name)
    await bot.send_message(callback.from_user.id, "Расписание успешно удалено.",
                           reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands=['help'])
async def help_command_h(message: types.Message):
    insert_into_online_db(message.chat.id)

    await bot.send_message(message.chat.id, "Я хз, что сюда добавить.")


@dp.message_handler(commands=['get_id'])
async def get_id_h(message: types.Message):
    insert_into_online_db(message.chat.id)
    await bot.send_message(message.chat.id, f"id: {message.chat.id}.")


@dp.message_handler(commands=['break'], state='*')
async def break_command_h(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.chat.id, "Введите желаемую команду.")


@dp.message_handler(commands=['get_online'], state='*')
async def get_online_command_h(message: types.Message, state: FSMContext):
    insert_into_online_db(message.chat.id)

    await bot.send_message(message.chat.id, 'Укажите период, за которой необходимо вывести статистику.')
    await state.set_state(OnlineStates.waiting_for_period.state)


@dp.message_handler(state=OnlineStates.waiting_for_period)
async def get_online_FSM_h(message: types.Message, state: FSMContext):
    try:
        online = get_online(message.text)
        if 0 < int(message.text) <= DAYS_TO_STORE:
            text = f"Онлайн за указанный период: {len(online)}."
        else:
            text = f"Мы храним информацию о пользователях не более чем {DAYS_TO_STORE} дней."
        await bot.send_message(message.chat.id, text)
    except ValueError:
        await bot.send_message(message.chat.id, "Необходимо ввести число, а не эту фигню фигню выше.")
    finally:
        await state.finish()


@dp.message_handler(commands=['create_schedule'], state='*')
async def preparation_level_st_h(message: types.Message, state: FSMContext):
    insert_into_online_db(message.chat.id)

    await bot.send_message(message.chat.id, 'Выбери уровень подготовки.',
                           reply_markup=common_kb.group_keyboard_list_reply(
                               ["Бакалавриат", "Магистратура", "Специалитет"]))
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

    await bot.send_message(message.chat.id, 'Придумайте название своему расписанию.',
                           reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(ScheduleStatesStudents.waiting_for_schedule_name.state)


@dp.message_handler(state=ScheduleStatesStudents.waiting_for_schedule_name)
async def adding_data_st_h(message: types.Message, state: FSMContext):
    if "'" in message.text:
        await bot.send_message(message.chat.id, "Название расписания не должно содержать апострофы.")
        await state.finish()
        return

    data_dict_values = list(DATA_DICT.values())

    await bot.send_message(message.chat.id, insert_into_client_db(message.chat.id, message.text, data_dict_values),
                           reply_markup=types.ReplyKeyboardRemove())

    await state.finish()


async def kinda_validator(message, state, elems, err_message):
    if message.text not in elems:
        await bot.send_message(message.chat.id, err_message)
        await state.finish()
        return True
    return False


@dp.message_handler(commands=['delete_my_schedule'], state='*')
async def delete_client_schedule_h(message: types.Message, state: FSMContext):
    insert_into_online_db(message.chat.id)

    schedule = get_client_schedule_names(message.chat.id)
    if schedule is None:
        await bot.send_message(message.chat.id, "У вас нет ни одного расписания.")
        await state.finish()
        return

    async with state.proxy() as proxy_data:
        proxy_data['names_to_validate'] = list(schedule.keys())

    await bot.send_message(message.chat.id, 'Выберите расписание.',
                           reply_markup=common_kb.group_keyboard_dict_reply(schedule))
    await state.set_state(ClientScheduleStates.waiting_for_schedule_to_delete.state)


@dp.message_handler(state=ClientScheduleStates.waiting_for_schedule_to_delete)
async def delete_client_schedule_wait_for_schedule_h(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy_data:
        names_to_validate = proxy_data["names_to_validate"]
    if await kinda_validator(message, state, names_to_validate, "Такого расписания не существует."):
        return

    delete_client_schedule(message.chat.id, message.text)
    await bot.send_message(message.chat.id, "Расписание успешно удалено.", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()
