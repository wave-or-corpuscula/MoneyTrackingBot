from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class MainMenuActions(Enum):
    money_tracking = "money_tracking"
    habits_tracking = "habits_tracking"


class MainMenuCbData(CallbackData, prefix="main_menu"):
    action : MainMenuActions


main_menu_list = [
    [InlineKeyboardButton(text="💰 Контроль трат", callback_data=MainMenuCbData(action=MainMenuActions.money_tracking).pack())],
    [InlineKeyboardButton(text="⌚ Контроль привычек", callback_data=MainMenuCbData(action=MainMenuActions.habits_tracking).pack())],
]

builder = InlineKeyboardBuilder(markup=main_menu_list)
main_menu_kb = builder.as_markup()
