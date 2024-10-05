from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.misc.callback_data.navigation import NavigationCbData, NavigationActions
from tgbot.keyboards.money_tracker.spending_types_kb import SpendingTypesCbData


class EditSpendingActions(Enum):
    edit_spending_type = "edit_spending_type"
    edit_spending_price = "edit_spending_price"
    edit_spending_description = "edit_spending_description"


class EditSpendingCbData(CallbackData, prefix="edit_spending"):
    action : EditSpendingActions


edit_spending_kb_list = [
    [
        InlineKeyboardButton(text="📓 Изменить категорию", callback_data=EditSpendingCbData(action=EditSpendingActions.edit_spending_type).pack())
    ],
    [
        InlineKeyboardButton(text="💵 Изменить сумму", callback_data=EditSpendingCbData(action=EditSpendingActions.edit_spending_price).pack())
    ],
    [
        InlineKeyboardButton(text="📑 Изменить описание", callback_data=EditSpendingCbData(action=EditSpendingActions.edit_spending_description).pack())
    ],
    [
        InlineKeyboardButton(text="↩️ Назад", callback_data=NavigationCbData(navigation=NavigationActions.back).pack())
    ]
]

builder = InlineKeyboardBuilder(markup=edit_spending_kb_list)
edit_spending_kb = builder.as_markup()
