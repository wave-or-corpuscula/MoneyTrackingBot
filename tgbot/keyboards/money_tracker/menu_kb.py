from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.misc.callback_data.navigation import NavigationCbData, NavigationActions


class MenuActions(Enum):
    add_spending = "add_spending"
    show_stats = "show_stats"
    settings = "settings"
    edit_spendings = "edit_spendings"
    about = "about"


class MenuCbData(CallbackData, prefix="money_tracker_menu"):
    action : MenuActions
    

money_tracker_menu_list = [
    [InlineKeyboardButton(text="💵 Добавить трату", callback_data=MenuCbData(action=MenuActions.add_spending).pack())],
    [InlineKeyboardButton(text="📝 Статистика трат", callback_data=MenuCbData(action=MenuActions.show_stats).pack())],
    [InlineKeyboardButton(text="✏️ Редактировать траты", callback_data=MenuCbData(action=MenuActions.edit_spendings).pack())],
    [InlineKeyboardButton(text="⚙️ Настройки", callback_data=MenuCbData(action=MenuActions.settings).pack())],
    [InlineKeyboardButton(text="ℹ️ О боте", callback_data=MenuCbData(action=MenuActions.about).pack())],
]

builder = InlineKeyboardBuilder(markup=money_tracker_menu_list)
money_tracker_menu_kb = builder.as_markup()