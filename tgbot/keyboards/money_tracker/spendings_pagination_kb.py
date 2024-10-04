from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.misc.callback_data.navigation import NavigationCbData, NavigationActions


class PaginationActions(Enum):
    next = "next"
    previous = "previous"
    goto = "goto"
    edit = "edit"
    delete = "delete"


class PaginationCbData(CallbackData, prefix="pagination"):
    action : PaginationActions


spendings_pagination_list = [
    [
        InlineKeyboardButton(text="⬅️", callback_data=PaginationCbData(action=PaginationActions.previous).pack()),
        InlineKeyboardButton(text="Перейти ⤵️", callback_data=PaginationCbData(action=PaginationActions.goto).pack()),
        InlineKeyboardButton(text="➡️", callback_data=PaginationCbData(action=PaginationActions.next).pack()),
    ],
    [
        InlineKeyboardButton(text="✏️", callback_data=PaginationCbData(action=PaginationActions.edit).pack()),
        InlineKeyboardButton(text="❌", callback_data=PaginationCbData(action=PaginationActions.delete).pack()),
    ],
    [
        InlineKeyboardButton(text="↩️ Назад", callback_data=NavigationCbData(navigation=NavigationActions.back).pack()),
    ]
]

builder = InlineKeyboardBuilder(markup=spendings_pagination_list)
spendings_pagination_kb = builder.as_markup()