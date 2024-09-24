from aiogram.fsm.state import StatesGroup, State


class MainMenuStates(StatesGroup):
    choosing_service = State()
    finance_controller = State()
    habit_tracking = State()