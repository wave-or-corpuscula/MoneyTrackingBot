from aiogram import types, F, Router, Bot
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.utils.formatting import as_list, Italic

from tgbot.models import SpendingType
from tgbot.utils import Database, ScreenManager
from tgbot.states import MainMenuStates, MoneyTrackerStates

from tgbot.misc.callback_data import MoneyTrackerCallbackData, CommonCallbackData
from tgbot.misc.callback_data.navigation import NavigationActions, NavigationCbData


from tgbot.keyboards.money_tracker_keyboards import kb_statistics, kb_spending_types


money_tracker_router = Router(name=__name__)


@money_tracker_router.callback_query(F.data == CommonCallbackData.MONEY_TRACKER.value, 
                                     StateFilter(MainMenuStates.choosing_service))
async def money_tracker_main_menu(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MoneyTrackerStates.choosing_service)
    await callback.message.edit_text(**ScreenManager.MONEY_TRACKER_MENU.as_kwargs())


@money_tracker_router.callback_query(
        NavigationCbData.filter(F.navigation == NavigationActions.back), 
        StateFilter(MoneyTrackerStates.choosing_service)
)
async def back_to_main_menu(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MainMenuStates.choosing_service)
    await callback.message.edit_text(**ScreenManager.START_SCREEN.as_kwargs())


@money_tracker_router.callback_query(F.data == MoneyTrackerCallbackData.ADD_SPENDING.value,
                                     StateFilter(MoneyTrackerStates.choosing_service))
async def add_spending_script(callback: types.CallbackQuery, state: FSMContext):
    await state.set_data({"chat_id": callback.message.chat.id, "message_id": callback.message.message_id})
    await state.set_state(MoneyTrackerStates.choose_spending_type)
    await callback.message.edit_text(**ScreenManager.SPENDING_TYPE_CHOOSING.as_kwargs(user_id=callback.from_user.id))


@money_tracker_router.callback_query(F.data == MoneyTrackerCallbackData.SHOW_STATS.value,
                                     StateFilter(MoneyTrackerStates.choosing_service))
async def show_statistics(callback: types.CallbackQuery, state: FSMContext, db: Database):
    await state.set_state(MoneyTrackerStates.statistics)
    await callback.message.edit_text(**ScreenManager.SHOW_STATISTICS.as_kwargs(user_id=callback.from_user.id, db=db))


@money_tracker_router.callback_query(F.data == MoneyTrackerCallbackData.SETTINGS.value,
                                     StateFilter(MoneyTrackerStates.choosing_service))
async def show_settings(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MoneyTrackerStates.choosing_setting)
    await callback.message.edit_text(**ScreenManager.SETTINGS_MENU.as_kwargs())

