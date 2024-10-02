import os

import logging

from aiogram import types, F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from tgbot.utils import Database, Multitool, ScreenManager
from tgbot.states import MainMenuStates, MoneyTrackerStates
from tgbot.misc.callback_data.navigation import NavigationActions, NavigationCbData

from tgbot.keyboards.money_tracker.statistics_kb import MTStatisticsActions, MTStatisticsCbData


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
async def get_report(callback: types.CallbackQuery, state: FSMContext, bot: Bot, db: Database):
    await callback.message.edit_text(**ScreenManager.REPORT_FORMING.as_kwargs())
    filename = Multitool.create_excel_report(callback.from_user.id, callback.from_user.full_name)
    file = types.FSInputFile(filename)
    await bot.send_document(callback.message.chat.id, document=file)
    os.remove(filename)
    await state.set_state(MoneyTrackerStates.statistics)
    await bot.send_message(chat_id=callback.message.chat.id,
                           **ScreenManager.SHOW_STATISTICS.as_kwargs(user_id=callback.from_user.id, db=db))
