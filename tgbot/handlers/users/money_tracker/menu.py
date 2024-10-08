from aiogram import types, F, Router, Bot
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.enums.content_type import ContentType

from tgbot.utils import Database, ScreenManager
from tgbot.states import MoneyTrackerStates
from tgbot.filters import ValidSpendingFilter
from tgbot.middlewares import DescriptionExtractMiddleware

from tgbot.misc.callback_data.navigation import NavigationActions, NavigationCbData
from tgbot.keyboards.money_tracker.spending_types_kb import SpendingTypesCbData
from tgbot.keyboards.money_tracker.menu_kb import MoneyTrackerMenuActions, MoneyTrackerMenuCbData


money_tracker_router = Router(name=__name__)

money_tracker_router.message.middleware(DescriptionExtractMiddleware())


@money_tracker_router.callback_query(
    StateFilter(MoneyTrackerStates.choosing_service),
    MoneyTrackerMenuCbData.filter(F.action == MoneyTrackerMenuActions.about),
)
async def show_about(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MoneyTrackerStates.about_shown)
    await callback.message.edit_text(**ScreenManager.SHOW_ABOUT.as_kwargs())


@money_tracker_router.callback_query(
    StateFilter(MoneyTrackerStates.about_shown),
    NavigationCbData.filter(F.navigation == NavigationActions.back)
)
async def show_about(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MoneyTrackerStates.choosing_service)
    await callback.message.edit_text(**ScreenManager.MONEY_TRACKER_MENU.as_kwargs())


@money_tracker_router.callback_query(
    StateFilter(MoneyTrackerStates.choosing_service),
    MoneyTrackerMenuCbData.filter(F.action == MoneyTrackerMenuActions.show_stats)
)
async def show_statistics(callback: types.CallbackQuery, state: FSMContext, db: Database):
    await state.set_state(MoneyTrackerStates.statistics)
    await callback.message.edit_text(**ScreenManager.SHOW_STATISTICS.as_kwargs(user_id=callback.from_user.id, db=db))


@money_tracker_router.callback_query(
    StateFilter(MoneyTrackerStates.choosing_service),
    MoneyTrackerMenuCbData.filter(F.action == MoneyTrackerMenuActions.settings)
)
async def show_settings(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MoneyTrackerStates.choosing_setting)
    await callback.message.edit_text(**ScreenManager.SETTINGS_MENU.as_kwargs())


# --- Добавление трат из главного меню --- #

@money_tracker_router.message(
    StateFilter(MoneyTrackerStates.choosing_service),
    F.content_type == ContentType.TEXT,
    ValidSpendingFilter()
)
async def add_spending_shortcut(message: Message, state: FSMContext, spending: float, description: str, bot: Bot):
    data = await state.get_data()
    message_id = data.get("main_message_id")
    await state.update_data({"spending": spending, "description": description})
    await state.set_state(MoneyTrackerStates.choose_spending_type_shortcut)
    await bot.edit_message_text(chat_id=message.chat.id,
                                message_id=message_id,
                                **ScreenManager.SHORTCUT_CHOOSE_SPENDING_TYPE.as_kwargs(user_id=message.from_user.id))
    await message.delete()

# Отмена
@money_tracker_router.callback_query(
    StateFilter(MoneyTrackerStates.choose_spending_type_shortcut),
    NavigationCbData.filter(F.navigation == NavigationActions.back)
)
async def cancel_add_spending_shortcut(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MoneyTrackerStates.choosing_service)
    await callback.message.edit_text(**ScreenManager.MONEY_TRACKER_MENU.as_kwargs())


@money_tracker_router.callback_query(
    StateFilter(MoneyTrackerStates.choose_spending_type_shortcut),
    SpendingTypesCbData.filter()
)
async def choosing_spending_type_shortcut(callback: types. CallbackQuery, callback_data: SpendingTypesCbData, state: FSMContext, db: Database, bot: Bot):
    data = await state.get_data()
    spending = data.get("spending")
    description = data.get("description")
    db.add_spending(user_id=callback.from_user.id, 
                    spending_type_id=callback_data.type_id, 
                    spending=spending, 
                    description=description)
    await state.set_state(MoneyTrackerStates.choosing_service)
    await callback.message.edit_text(**ScreenManager.MAIN_MENU_FROM_SHORTCUT.as_kwargs(spending=spending))
