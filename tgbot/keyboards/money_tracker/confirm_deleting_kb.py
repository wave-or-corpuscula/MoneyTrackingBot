from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.misc.callback_data.navigation import NavigationCbData, NavigationActions
from tgbot.keyboards.money_tracker.edit_spending_types_kb import EditSpendingTypeActions, EditSpendingTypeCbData


confirm_deleting_list = [
    [
        InlineKeyboardButton(text="✅ Удалить", callback_data=EditSpendingTypeCbData(action=EditSpendingTypeActions.delete).pack()),
        InlineKeyboardButton(text="❌ Отмена", callback_data=NavigationCbData(navigation=NavigationActions.back).pack()),
    ]
]

builder = InlineKeyboardBuilder(markup=confirm_deleting_list)
confirm_deleting_kb = builder.as_markup()