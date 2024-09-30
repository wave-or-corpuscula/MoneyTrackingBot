from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.utils import Database
from tgbot.misc.callback_data.navigation import NavigationActions, NavigationCbData


class SpendingTypesCbData(CallbackData, prefix="spending_type"):
    type_id : int


def build_spending_types_kb(**kwargs) -> InlineKeyboardMarkup:
    user_id = kwargs.get("user_id")
    builder = InlineKeyboardBuilder()
    user_types = Database.get_user_spending_types(user_id)
    
    for user_type in user_types:
        builder.button(text=user_type.type_name, callback_data=SpendingTypesCbData(type_id=user_type.id).pack())
    builder.button(text="↩️ Назад", callback_data=NavigationCbData(navigation=NavigationActions.back).pack())
    builder.adjust(1)
    return builder.as_markup()