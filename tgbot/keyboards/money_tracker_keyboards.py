from tgbot.models import SpendingType

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.utils import Database
from tgbot.misc.callback_data import MoneyTrackerCallbackData, CommonCallbackData

from tgbot.misc.callback_data.navigation import NavigationCbData, NavigationActions


kb_money_tracker_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💵 Добавить трату", callback_data=MoneyTrackerCallbackData.ADD_SPENDING)],
    [InlineKeyboardButton(text="📝 Статистика трат", callback_data=MoneyTrackerCallbackData.SHOW_STATS)],
    [InlineKeyboardButton(text="⚙️ Настройки", callback_data=MoneyTrackerCallbackData.SETTINGS)],
    [InlineKeyboardButton(text="↩️ Назад", callback_data=NavigationCbData(navigation=NavigationActions.back).pack())],
])
 
kb_statistics = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📑 Полный отчет", callback_data=MoneyTrackerCallbackData.STATISTICS_GET_REPORT)],
    [InlineKeyboardButton(text="↩️ Назад", callback_data=MoneyTrackerCallbackData.BACK)],
])

def kb_spending_types(**kwargs) -> InlineKeyboardMarkup:
    user_id = kwargs.get("user_id")
    
    user_types = Database.get_user_spending_types(user_id)
    builder = []
    for user_type in user_types:
        builder.append([InlineKeyboardButton(text=user_type.type_name, callback_data=f"{user_type.id}")])
    builder.append([InlineKeyboardButton(text="↩️ Назад", callback_data=NavigationCbData(navigation=NavigationActions.back).pack())])
    return InlineKeyboardMarkup(inline_keyboard=builder)

kb_settings_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Типы трат", callback_data=MoneyTrackerCallbackData.SETTINDS_EDIT_SPENDING_TYPES)],
    [InlineKeyboardButton(text="↩️ Назад", callback_data=MoneyTrackerCallbackData.BACK)],
])

# def kb_settings_spending_types_edit(**kwargs) ->InlineKeyboardMarkup:
#     user_id = kwargs.get("user_id")
#     user_types = Database.get_user_spending_types(user_id)
#     builder = []
#     for user_type in user_types:
#         builder.append([
#             InlineKeyboardButton(text=user_type.type_name, callback_data=f"{user_type.id}"),
#             InlineKeyboardButton(text="✏️", callback_data=f"edit:{user_type.id}"),
#             InlineKeyboardButton(text="❌", callback_data=f"delete:{user_type.id}"),
#         ])
#     builder.append([InlineKeyboardButton(text="↩️ Назад", callback_data=MoneyTrackerCallbackData.BACK)])
#     return InlineKeyboardMarkup(inline_keyboard=builder)

