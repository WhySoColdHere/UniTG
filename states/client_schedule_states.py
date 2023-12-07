from aiogram.dispatcher.filters.state import State, StatesGroup


class ClientScheduleStates(StatesGroup):
    waiting_for_schedule_to_show = State()
    waiting_for_schedule_to_delete = State()
