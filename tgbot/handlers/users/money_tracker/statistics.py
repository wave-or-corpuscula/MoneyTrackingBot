import logging

from aiogram import types, F, Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.utils.formatting import as_list, Italic

from tgbot.utils import Database, Multitool, ScreenManager
from tgbot.states import MainMenuStates, MoneyTrackerStates
from tgbot.misc.callback_data.navigation import NavigationActions, NavigationCbData

from tgbot.keyboards.money_tracker.statistics_kb import statistics_kb, MTStatisticsActions, MTStatisticsCbData


statistics_router = Router(name=__name__)


@statistics_router.callback_query(
        NavigationCbData.filter(F.navigation == NavigationActions.back),
        StateFilter(MoneyTrackerStates.statistics)
)
async def back_from_stats(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MoneyTrackerStates.choosing_service)
    await callback.message.edit_text(**ScreenManager.MONEY_TRACKER_MENU.as_kwargs())


@statistics_router.callback_query(
        MTStatisticsCbData.filter(F.action == MTStatisticsActions.get_report),
        StateFilter(MoneyTrackerStates.statistics)
)
async def get_report(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(Multitool.feature_in_process_text(callback), reply_markup=statistics_kb)