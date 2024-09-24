from aiogram.fsm.state import StatesGroup, State


class MoneyTrackerMenuStates(StatesGroup):
    choosing_service = State()
    add_spending = State()
    show_stats = State()
    settings = State()
