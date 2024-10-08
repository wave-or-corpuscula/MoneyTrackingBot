from aiogram.fsm.state import StatesGroup, State


class MoneyTrackerStates(StatesGroup):
    choosing_service = State()
    add_spending = State()
    choose_spending_type = State()
    show_stats = State()
    statistics = State()
    about_shown = State()

    choosing_setting = State()
    
    spending_types_edit_list = State()
    spending_type_edit_choosed = State()
    spending_type_enter_new = State()
    spending_type_edit_enter_new = State()
    spending_type_deleting_confirm = State()

    # --- Spendings pagination --- #

    spendings_pagination = State()
    enter_spending_page = State()
    editing_spending = State()
    enter_new_spending_price = State()
    enter_new_description = State()
    enter_new_spending_type = State()

    # --- Shortcut spending adding --- #

    choose_spending_type_shortcut = State()

    

