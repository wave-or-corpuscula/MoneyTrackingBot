import logging

from aiogram import types, F, Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.utils.formatting import as_list, Italic

from tgbot.states import MainMenuStates, MoneyTrackerStates
from tgbot.misc.callback_data import MoneyTrackerCallbackData, CommonCallbackData

from tgbot.keyboards import kb_main_menu, kb_back
from tgbot.keyboards.money_tracker_keyboards import kb_money_tracker_menu, kb_statistics
from tgbot.utils import Database, Multitool, ScreenManager


statistics_router = Router(name=__name__)


@statistics_router.callback_query(F.data == MoneyTrackerCallbackData.BACK.value,
                                  StateFilter(MoneyTrackerStates.statistics))
async def back_from_stats(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MoneyTrackerStates.choosing_service)
    await callback.message.edit_text(**ScreenManager.MONEY_TRACKER_MENU.as_kwargs())

@statistics_router.callback_query(F.data == MoneyTrackerCallbackData.STATISTICS_GET_REPORT.value,
                                  StateFilter(MoneyTrackerStates.statistics))
async def get_report(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(Multitool.feature_in_process_text(callback), reply_markup=kb_statistics)