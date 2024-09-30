from aiogram.fsm.state import StatesGroup, State


class MoneyTrackerStates(StatesGroup):
    choosing_service = State()
    add_spending = State()
    choose_spending_type = State()
    show_stats = State()
    choosing_setting = State()
    statistics = State()
    
    spending_types_edit_list = State()
    spending_type_edit_choosed = State()
    spending_type_enter_new = State()
    spending_type_edit_enter_new = State()
