from aiogram.fsm.state import StatesGroup, State


class MoneyTrackerStates(StatesGroup):
    choosing_service = State()
    add_spending = State()
    choose_spending_type = State()
    show_stats = State()
    choosing_setting = State()
    statistics = State()
    
    editing_spending_types = State()
