from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.utils import Database
from tgbot.misc.callback_data.navigation import NavigationCbData, NavigationActions
from tgbot.keyboards.money_tracker.spending_types_kb import SpendingTypesCbData


class EditSpendingTypeActions(Enum):
    edit = "edit"
    delete = "delete"
    new = "new"
    no_action = "no_action"


class EditSpendingTypeCbData(CallbackData, prefix="spending_type"):
    action : EditSpendingTypeActions


edit_spending_type_list = [
    [
        InlineKeyboardButton(text="✏️", callback_data=EditSpendingTypeCbData(action=EditSpendingTypeActions.edit).pack()),
        InlineKeyboardButton(text="❌", callback_data=EditSpendingTypeCbData(action=EditSpendingTypeActions.delete).pack()),
    ],
    [InlineKeyboardButton(text="↩️ Назад", callback_data=NavigationCbData(navigation=NavigationActions.back).pack())]
]

builder = InlineKeyboardBuilder(markup=edit_spending_type_list)
edit_spending_type_kb = builder.as_markup()


def build_spending_types_for_edit_kb(**kwargs) ->InlineKeyboardMarkup:
    user_id = kwargs.get("user_id")
    user_types = Database.get_user_spending_types(user_id)
    builder = InlineKeyboardBuilder()
    for user_type in user_types:
        builder.button(text=user_type.type_name, callback_data=SpendingTypesCbData(type_id=user_type.id).pack())
    builder.button(text="➕ Новый тип", callback_data=EditSpendingTypeCbData(action=EditSpendingTypeActions.new).pack())
    builder.button(text="↩️ Назад", callback_data=NavigationCbData(navigation=NavigationActions.back).pack())
    builder.adjust(1)
    return builder.as_markup()