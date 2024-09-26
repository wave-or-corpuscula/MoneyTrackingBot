from aiogram import types, F, Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.utils.formatting import as_list, Italic

from tgbot.utils import Database, ScreenManager
from tgbot.states import MainMenuStates, MoneyTrackerStates
from tgbot.misc.callback_data import MoneyTrackerCallbackData, CommonCallbackData


from tgbot.keyboards.money_tracker_keyboards import kb_statistics


money_tracker_router = Router(name=__name__)


@money_tracker_router.callback_query(F.data == CommonCallbackData.MONEY_TRACKER.value, 
                                     StateFilter(MainMenuStates.choosing_service))
async def money_tracker_main_menu(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MoneyTrackerStates.choosing_service)
    await callback.message.edit_text(**ScreenManager.MONEY_TRACKER_MENU.as_kwargs())


@money_tracker_router.callback_query(F.data == MoneyTrackerCallbackData.BACK.value, 
                                     StateFilter(MoneyTrackerStates.choosing_service))
async def back_to_main_menu(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MainMenuStates.choosing_service)
    await callback.message.edit_text(**ScreenManager.START_SCREEN.as_kwargs())


@money_tracker_router.callback_query(F.data == MoneyTrackerCallbackData.ADD_SPENDING.value,
                                     StateFilter(MoneyTrackerStates.choosing_service))
async def add_spending_script(callback: types.CallbackQuery, state: FSMContext):
    await state.set_data({"chat_id": callback.message.chat.id, "message_id": callback.message.message_id})
    await state.set_state(MoneyTrackerStates.choose_spending_type)

    await callback.message.edit_text(**ScreenManager.SPENDING_TYPE_CHOOSING.as_kwargs())

@money_tracker_router.callback_query(F.data == MoneyTrackerCallbackData.SHOW_STATS.value,
                                     StateFilter(MoneyTrackerStates.choosing_service))
async def show_statistics(callback: types.CallbackQuery, state: FSMContext, db: Database):

    week_spend = db.get_week_spending(callback.from_user.id)
    month_spend = db.get_month_spending(callback.from_user.id)
    
    text = [
        "<b>Статистика</b>\n",
        f"<i>Траты за месяц: <u>{month_spend}</u></i>",
        f"<i>Траты за неделю: <u>{week_spend}</u></i>",
    ]

    await state.set_state(MoneyTrackerStates.statistics)
    await callback.message.edit_text("\n".join(text), reply_markup=kb_statistics)


@money_tracker_router.callback_query(F.data == MoneyTrackerCallbackData.SETTINGS.value,
                                     StateFilter(MoneyTrackerStates.choosing_service))
async def show_settings(callback: types.CallbackQuery, state: FSMContext):

    await state.set_state(MoneyTrackerStates.settings)
    await callback.message.edit_text(**ScreenManager.SETTINGS_MENU.as_kwargs())

