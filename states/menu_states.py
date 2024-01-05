from aiogram.dispatcher.filters.state import State, StatesGroup


class MenuCommandStates(StatesGroup):
    waiting_for_button_click = State()
