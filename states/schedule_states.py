from aiogram.dispatcher.filters.state import State, StatesGroup


class ScheduleStates(StatesGroup):
    waiting_for_role = State()
    waiting_for_institute = State()
    waiting_for_course = State()
    waiting_for_educational_form = State()
    waiting_for_group = State()

# Институт --> Курс --> Форма обучения (оч/заоч/оч-заоч) --> Выбор группы.
# Парсер.
