from enum import Enum


class MoneyTrackerCallbackData(Enum):
    ADD_SPENDING = "add_spending"
    SHOW_STATS = "show_stats"
    SETTINGS = "settings"

    STATISTICS_GET_REPORT = "statistics_get_report"

    BACK = "back"
