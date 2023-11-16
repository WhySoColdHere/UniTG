from aiogram import types
from keyboards import common_kb, common_keyboard_names
from create_bot import bot, dp
from aiogram.dispatcher import FSMContext
from states.schedule_states import ScheduleStatesStudents

DATA = []


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(message.chat.id, 'Здарова! Бот твоей шараги. Помощь по командам /help')


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await bot.send_message(message.chat.id, "You are loool")


#######################################

async def kinda_validator_st(message, elems, err_message):
    if message.text not in elems:
        await bot.send_message(message.chat.id, err_message)
        return


@dp.message_handler(commands=['show_schedule'], state='*')
async def role_schedule_st(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, 'Выбери роль',
                           reply_markup=common_kb.group_keyboard_common_reply(
                               common_keyboard_names.roles()))
    await state.set_state(ScheduleStatesStudents.waiting_for_role.state)


@dp.message_handler(state=ScheduleStatesStudents.waiting_for_role)
async def institute_schedule_st(message: types.Message, state: FSMContext):
    await kinda_validator_st(message, common_keyboard_names.roles(), "Выберите существующую роль!")
    await state.update_data(role_st=message.text)
    DATA.append(message.text)

    await bot.send_message(message.chat.id, 'Выбери уровень подготовки',
                           reply_markup=common_kb.group_keyboard_common_reply(
                               common_keyboard_names.levels_of_preparation()))
    await state.set_state(ScheduleStatesStudents.waiting_for_level_of_preparation.state)


@dp.message_handler(state=ScheduleStatesStudents.waiting_for_level_of_preparation)
async def course_schedule_st(message: types.Message, state: FSMContext):
    await kinda_validator_st(message, common_keyboard_names.levels_of_preparation(), "Выберите уровень подготовки!")
    await state.update_data(level_of_preparation_st=message.text)
    DATA.append(message.text)

    await bot.send_message(message.chat.id, 'Выбери институт',
                           reply_markup=common_kb.group_keyboard_common_reply(
                               common_keyboard_names.institutes()))
    await state.set_state(ScheduleStatesStudents.waiting_for_institute.state)


@dp.message_handler(state=ScheduleStatesStudents.waiting_for_institute)
async def education_form_schedule_st(message: types.Message, state: FSMContext):
    await kinda_validator_st(message, common_keyboard_names.institutes(), "Выберите существующий институт!")
    await state.update_data(course_st=message.text)
    DATA.append(message.text)

    await bot.send_message(message.chat.id, 'Выбери курс',
                           reply_markup=common_kb.group_keyboard_common_reply(
                               common_keyboard_names.courses()))
    await state.set_state(ScheduleStatesStudents.waiting_for_course.state)


@dp.message_handler(state=ScheduleStatesStudents.waiting_for_course)
async def group_schedule_st(message: types.Message, state: FSMContext):
    await kinda_validator_st(message, common_keyboard_names.courses(),
                             "Выберите существующий курс!")
    await state.update_data(educational_form_st=message.text)
    DATA.append(message.text)

    await bot.send_message(message.chat.id, 'Выбери форму обучения',
                           reply_markup=common_kb.group_keyboard_common_reply(
                               common_keyboard_names.education_forms()))
    await state.set_state(ScheduleStatesStudents.waiting_for_educational_form.state)


@dp.message_handler(state=ScheduleStatesStudents.waiting_for_educational_form)
async def final_schedule_st(message: types.Message, state: FSMContext):
    await kinda_validator_st(message, common_keyboard_names.education_forms(), "Выбери существующую форму обучения!")
    await state.update_data(group_st=message.text)
    DATA.append(message.text)

    await bot.send_message(message.chat.id, 'Выбери группу',
                           reply_markup=common_kb.group_keyboard_common_reply(
                               common_keyboard_names.groups()))
    await state.set_state(ScheduleStatesStudents.waiting_for_group.state)


@dp.message_handler(state=ScheduleStatesStudents.waiting_for_group)
async def final_schedule_st(message: types.Message, state: FSMContext):
    await kinda_validator_st(message, common_keyboard_names.groups(), "Выбери существующую группу!")
    await state.update_data(group_st=message.text)
    DATA.append(message.text)

    await bot.send_message(message.chat.id, DATA)
    # Сохраняем куда-нибудь запрос из DATA, дабы потом многократно к нему обращаться.

    # Тактика такая: У нас статичен только список институтов.
    # Как только мы его получаем, сразу обращаемся к бд, и выводим остальную инфу, на основе предыдущего 'узла', тк
    # в их расписании все связано.
