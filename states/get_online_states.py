from aiogram.dispatcher.filters.state import State, StatesGroup


class OnlineStates(StatesGroup):
    waiting_for_period = State()
