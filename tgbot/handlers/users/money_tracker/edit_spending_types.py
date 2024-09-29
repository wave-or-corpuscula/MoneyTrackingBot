import logging

from aiogram import types, F, Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.utils.formatting import as_list, Italic

from tgbot.states import MainMenuStates, MoneyTrackerStates
from tgbot.misc.callback_data import MoneyTrackerCallbackData, CommonCallbackData

from tgbot.utils import Database, ScreenManager


edit_spending_types_router = Router(name=__name__)


@edit_spending_types_router.callback_query(F.data == MoneyTrackerCallbackData.SETTINDS_EDIT_SPENDING_TYPES.value,
                                           StateFilter(MoneyTrackerStates.choosing_setting))
async def show_spending_types_edit(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MoneyTrackerStates.editing_spending_types)
    await callback.message.edit_text(**ScreenManager.SETTINGS_EDIT_SPENDING_TYPES.as_kwargs(user_id=callback.from_user.id))

@edit_spending_types_router.callback_query(F.data == MoneyTrackerCallbackData.BACK.value,
                                           StateFilter(MoneyTrackerStates.editing_spending_types))
async def cancel_editing_spending_types(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MoneyTrackerStates.choosing_setting)
    await callback.message.edit_text(**ScreenManager.SETTINGS_MENU.as_kwargs())