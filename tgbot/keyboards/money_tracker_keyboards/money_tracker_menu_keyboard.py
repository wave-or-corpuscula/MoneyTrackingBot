from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.misc.callback_data import MoneyTrackerCallbackData

kb_money_tracker_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Добавить трату", callback_data=MoneyTrackerCallbackData.ADD_SPENDING)],
    [InlineKeyboardButton(text="Статистика трат", callback_data=MoneyTrackerCallbackData.SHOW_STATS)],
    [InlineKeyboardButton(text="Настройки", callback_data=MoneyTrackerCallbackData.SETTINGS)],
])