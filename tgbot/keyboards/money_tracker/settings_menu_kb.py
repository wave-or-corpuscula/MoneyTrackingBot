from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.misc.callback_data.navigation import NavigationCbData, NavigationActions


class MTSettingsMenuActions(Enum):
    spending_types = "spending_types"
    edit_spendings = "edit_spendings"


class MTSettingsMenuCbData(CallbackData, prefix="mt_settings_menu"):
    action : MTSettingsMenuActions


settings_menu_list = [
    [InlineKeyboardButton(text="🖋️ Изменить категории", callback_data=MTSettingsMenuCbData(action=MTSettingsMenuActions.spending_types).pack())],
    [InlineKeyboardButton(text="↩️ Назад", callback_data=NavigationCbData(navigation=NavigationActions.back).pack())],
]

builder = InlineKeyboardBuilder(markup=settings_menu_list)
settings_menu_kb = builder.as_markup()
