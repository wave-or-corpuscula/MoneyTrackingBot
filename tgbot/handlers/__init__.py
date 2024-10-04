from .users import *

routers = [

    # Money tracker routers

    money_tracker_router,
    add_spending_router,
    statistics_router,
    settings_router,
    edit_spending_types_router,
    spendings_pagination_router,

    common_router,
]