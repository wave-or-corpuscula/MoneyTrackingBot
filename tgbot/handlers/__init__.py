from .users import *

routers = [

    # Money tracker routers

    money_tracker_router,
    add_spending_router,
    statistics_router,
    settings_router,

    # Habits tracker routers

    habits_tracker_router,

    common_router,
]