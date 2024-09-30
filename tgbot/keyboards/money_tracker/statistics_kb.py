from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.misc.callback_data.navigation import NavigationCbData, NavigationActions


class MTStatisticsActions(Enum):
    get_report = "get_report"


class MTStatisticsCbData(CallbackData, prefix="money_tracker_statistics"):
    action : MTStatisticsActions


statistics_list = [
    [InlineKeyboardButton(text="📑 Полный отчет", callback_data=MTStatisticsCbData(action=MTStatisticsActions.get_report).pack())],
    [InlineKeyboardButton(text="↩️ Назад", callback_data=NavigationCbData(navigation=NavigationActions.back).pack())],
]

builder = InlineKeyboardBuilder(markup=statistics_list)
statistics_kb = builder.as_markup()
