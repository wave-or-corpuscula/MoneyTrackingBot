from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.utils import Database
from tgbot.misc.callback_data import MoneyTrackerCallbackData


class SpendingTypeActions(Enum):
    edit = "edit"
    delete = "delete"
    no_action = "no_action"


class SpendingTypeCbData(CallbackData, prefix="spending_type"):
    type_id : int
    action : SpendingTypeActions


def build_spending_types_kb(**kwargs) ->InlineKeyboardMarkup:
    user_id = kwargs.get("user_id")
    user_types = Database.get_user_spending_types(user_id)
    builder = InlineKeyboardBuilder()
    for user_type in user_types:
        builder.button(text=user_type.type_name, callback_data=SpendingTypeCbData(type_id=user_type.id, action=SpendingTypeActions.no_action).pack())
        builder.button(text="✏️", callback_data=SpendingTypeCbData(type_id=user_type.id, action=SpendingTypeActions.edit).pack())
        builder.button(text="❌", callback_data=SpendingTypeCbData(type_id=user_type.id, action=SpendingTypeActions.delete).pack())
    builder.button(text="↩️ Назад", callback_data=MoneyTrackerCallbackData.BACK)
    builder.adjust(3, len(user_types))
    return builder.as_markup()