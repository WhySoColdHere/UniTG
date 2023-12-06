from aiogram.dispatcher.filters.state import State, StatesGroup


class ClientScheduleStates(StatesGroup):
    waiting_for_schedule = State()
