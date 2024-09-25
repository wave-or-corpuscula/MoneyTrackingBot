from tgbot.models import SpendingType

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.misc.callback_data import MoneyTrackerCallbackData, CommonCallbackData


kb_money_tracker_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💵 Добавить трату", callback_data=MoneyTrackerCallbackData.ADD_SPENDING)],
    [InlineKeyboardButton(text="📝 Статистика трат", callback_data=MoneyTrackerCallbackData.SHOW_STATS)],
    [InlineKeyboardButton(text="⚙️ Настройки", callback_data=MoneyTrackerCallbackData.SETTINGS)],
    [InlineKeyboardButton(text="↩️ Назад", callback_data=MoneyTrackerCallbackData.BACK)],
])

kb_statistics = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📑 Полный отчет", callback_data=MoneyTrackerCallbackData.STATISTICS_GET_REPORT)],
    [InlineKeyboardButton(text="↩️ Назад", callback_data=MoneyTrackerCallbackData.BACK)],
])

def kb_spending_types() -> InlineKeyboardMarkup:
    select_types = SpendingType.select()
    builder = []
    for type in select_types:
        builder.append([InlineKeyboardButton(text=type.type_name, callback_data=f"{type.id}")])
    builder.append([InlineKeyboardButton(text="↩️ Назад", callback_data=MoneyTrackerCallbackData.BACK)])
    return InlineKeyboardMarkup(inline_keyboard=builder)
