from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.misc.callback_data import CommonCallbackData


kb_main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🤑 Контроль трат", callback_data=CommonCallbackData.MONEY_TRACKER)],
    [InlineKeyboardButton(text="⌚ Контроль привычек", callback_data=CommonCallbackData.HABITS_TRACKER)],
])
