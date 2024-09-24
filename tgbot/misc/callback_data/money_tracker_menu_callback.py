from enum import Enum


class MoneyTrackerCallbackData(Enum):
    ADD_SPENDING = "add_spending"
    SHOW_STATS = "show_stats"
    SETTINGS = "settings"