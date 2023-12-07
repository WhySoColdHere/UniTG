from aiogram.dispatcher.filters.state import State, StatesGroup


class ScheduleStatesStudents(StatesGroup):
    waiting_for_institute = State()
    waiting_for_level_of_preparation = State()
    waiting_for_course = State()
    waiting_for_educational_form = State()
    waiting_for_group = State()
    waiting_for_schedule_name = State()
