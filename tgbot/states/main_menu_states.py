from aiogram.fsm.state import StatesGroup, State


class MainMenuState(StatesGroup):
    finance_controller = State()
    habit_tracking = State()