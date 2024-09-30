from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.misc.callback_data.navigation import NavigationCbData, NavigationActions


class MoneyTrackerMenuActions(Enum):
    add_spending = "add_spending"
    show_stats = "show_stats"
    settings = "settings"


class MoneyTrackerMenuCbData(CallbackData, prefix="money_tracker_menu"):
    action : MoneyTrackerMenuActions
    

money_tracker_menu_list = [
    [InlineKeyboardButton(text="💵 Добавить трату", callback_data=MoneyTrackerMenuCbData(action=MoneyTrackerMenuActions.add_spending).pack())],
    [InlineKeyboardButton(text="📝 Статистика трат", callback_data=MoneyTrackerMenuCbData(action=MoneyTrackerMenuActions.show_stats).pack())],
    [InlineKeyboardButton(text="⚙️ Настройки", callback_data=MoneyTrackerMenuCbData(action=MoneyTrackerMenuActions.settings).pack())],
    [InlineKeyboardButton(text="↩️ Назад", callback_data=NavigationCbData(navigation=NavigationActions.back).pack())],
]

builder = InlineKeyboardBuilder(markup=money_tracker_menu_list)
money_tracker_menu_kb = builder.as_markup()