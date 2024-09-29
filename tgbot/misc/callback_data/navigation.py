from enum import Enum

from aiogram.filters.callback_data import CallbackData


class NavigationActions(Enum):
    back = "back"


class NavigationCbData(CallbackData, prefix="navigation"):
    navigation : NavigationActions

# MoneyTrackerCallbackData.BACK