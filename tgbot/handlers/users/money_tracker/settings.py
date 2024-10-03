import logging

from aiogram import types, F, Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.utils.formatting import as_list, Italic

from tgbot.states import MoneyTrackerStates
from tgbot.misc.callback_data.navigation import NavigationActions, NavigationCbData

from tgbot.utils import ScreenManager

from tgbot.keyboards.money_tracker.settings_menu_kb import MTSettingsMenuActions, MTSettingsMenuCbData


settings_router = Router(name=__name__)


@settings_router.callback_query(
        NavigationCbData.filter(F.navigation == NavigationActions.back),
        StateFilter(MoneyTrackerStates.choosing_setting)
)
async def cancel_settings(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MoneyTrackerStates.choosing_service)
    await callback.message.edit_text(**ScreenManager.MONEY_TRACKER_MENU.as_kwargs())


@settings_router.callback_query(
        MTSettingsMenuCbData.filter(F.action == MTSettingsMenuActions.spending_types),
        StateFilter(MoneyTrackerStates.choosing_setting)
)
async def show_spending_types_list_for_edit(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MoneyTrackerStates.spending_types_edit_list)
    await callback.message.edit_text(**ScreenManager.SETTINGS_EDIT_SPENDING_TYPES_LIST.as_kwargs(user_id=callback.from_user.id))
