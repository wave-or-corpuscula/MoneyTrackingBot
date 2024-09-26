from aiogram import types, F, Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.utils.formatting import as_list, Italic

from tgbot.utils import Database, ScreenManager, Multitool
from tgbot.states import MainMenuStates, MoneyTrackerStates
from tgbot.misc.callback_data import MoneyTrackerCallbackData, CommonCallbackData


habits_tracker_router = Router(name=__name__)


@habits_tracker_router.callback_query(F.data == CommonCallbackData.HABITS_TRACKER.value,
                                      StateFilter(MainMenuStates.choosing_service))
async def habits_tracker_menu(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(Multitool.feature_in_process_text(callback), reply_markup=callback.message.reply_markup)

