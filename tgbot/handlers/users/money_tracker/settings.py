import logging

from aiogram import types, F, Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.utils.formatting import as_list, Italic

from tgbot.states import MainMenuStates, MoneyTrackerStates
from tgbot.misc.callback_data import MoneyTrackerCallbackData, CommonCallbackData

from tgbot.utils import Database, ScreenManager


settings_router = Router(name=__name__)


@settings_router.callback_query(F.data == MoneyTrackerCallbackData.BACK.value,
                                StateFilter(MoneyTrackerStates.choosing_setting))
async def cancel_settings(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MoneyTrackerStates.choosing_service)
    await callback.message.edit_text(**ScreenManager.MONEY_TRACKER_MENU.as_kwargs())

