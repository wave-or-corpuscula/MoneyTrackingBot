from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from tgbot.utils import Database, ScreenManager
from tgbot.states import MoneyTrackerStates

from tgbot.misc.callback_data.navigation import NavigationActions, NavigationCbData
from tgbot.keyboards.money_tracker.menu_kb import MoneyTrackerMenuActions, MoneyTrackerMenuCbData


money_tracker_router = Router(name=__name__)


@money_tracker_router.callback_query(
        StateFilter(MoneyTrackerStates.choosing_service),
        MoneyTrackerMenuCbData.filter(F.action == MoneyTrackerMenuActions.about),
)
async def show_about(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MoneyTrackerStates.about_shown)
    await callback.message.edit_text(**ScreenManager.SHOW_ABOUT.as_kwargs())


@money_tracker_router.callback_query(
        StateFilter(MoneyTrackerStates.about_shown),
        NavigationCbData.filter(F.navigation == NavigationActions.back),
)
async def show_about(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MoneyTrackerStates.choosing_service)
    await callback.message.edit_text(**ScreenManager.MONEY_TRACKER_MENU.as_kwargs())


@money_tracker_router.callback_query(
        MoneyTrackerMenuCbData.filter(F.action == MoneyTrackerMenuActions.show_stats),
        StateFilter(MoneyTrackerStates.choosing_service)
)
async def show_statistics(callback: types.CallbackQuery, state: FSMContext, db: Database):
    await state.set_state(MoneyTrackerStates.statistics)
    await callback.message.edit_text(**ScreenManager.SHOW_STATISTICS.as_kwargs(user_id=callback.from_user.id, db=db))


@money_tracker_router.callback_query(
        MoneyTrackerMenuCbData.filter(F.action == MoneyTrackerMenuActions.settings),
        StateFilter(MoneyTrackerStates.choosing_service)
)
async def show_settings(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MoneyTrackerStates.choosing_setting)
    await callback.message.edit_text(**ScreenManager.SETTINGS_MENU.as_kwargs())

