from enum import Enum


class MoneyTrackerCallbackData(Enum):
    ADD_SPENDING = "add_spending"
    SHOW_STATS = "show_stats"

    STATISTICS_GET_REPORT = "statistics_get_report"

    SETTINGS = "settings"
    SETTINDS_EDIT_SPENDING_TYPES = "settings_edit_spending_types"

    BACK = "back"
