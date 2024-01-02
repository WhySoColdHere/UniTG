from aiogram.dispatcher.filters.state import State, StatesGroup


class StartCommandStates(StatesGroup):
    waiting_for_button_click = State()
