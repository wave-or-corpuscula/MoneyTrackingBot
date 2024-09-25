from aiogram import types, F, Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.utils.formatting import as_list, Italic

from tgbot.states import MainMenuStates, MoneyTrackerStates
from tgbot.misc.callback_data import MoneyTrackerCallbackData, CommonCallbackData

from tgbot.keyboards import kb_main_menu, kb_back
from tgbot.keyboards.money_tracker_keyboards import *


money_tracker_router = Router(name=__name__)


@money_tracker_router.callback_query(F.data == CommonCallbackData.MONEY_TRACKER.value, 
                                     StateFilter(MainMenuStates.choosing_service))
async def money_tracker_main_menu(callback: types.CallbackQuery, state: FSMContext):
    text = [
        "<b>Отслеживание трат</b>\n",
        "Выберите нужное:"
    ]
    await state.set_state(MoneyTrackerStates.choosing_service)
    await callback.message.edit_text("\n".join(text), reply_markup=kb_money_tracker_menu)


@money_tracker_router.callback_query(F.data == MoneyTrackerCallbackData.BACK.value, 
                                     StateFilter(MoneyTrackerStates.choosing_service))
async def back_to_main_menu(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MainMenuStates.choosing_service)
    await callback.message.edit_text("Выберите тип отслеживания:", reply_markup=kb_main_menu)


@money_tracker_router.callback_query(F.data == MoneyTrackerCallbackData.ADD_SPENDING.value,
                                     StateFilter(MoneyTrackerStates.choosing_service))
async def add_spending_script(callback: types.CallbackQuery, state: FSMContext):
    await state.set_data({"chat_id": callback.message.chat.id, "message_id": callback.message.message_id})
    await state.set_state(MoneyTrackerStates.choose_spending_type)

    await callback.message.edit_text("Выберите тип траты:", reply_markup=kb_spending_types())

@money_tracker_router.callback_query(F.data == MoneyTrackerCallbackData.SHOW_STATS.value,
                                     StateFilter(MoneyTrackerStates.choosing_service))
async def show_statistics(callback: types.CallbackQuery, state: FSMContext):
    # TODO: Implement statistics gathering
    text = [
        "<b>Статистика</b>\n",
        f"Траты за неделю: {10}",
        f"Траты за месяц: {100}",
    ]

    await state.set_state(MoneyTrackerStates.statistics)
    await callback.message.edit_text("\n".join(text), reply_markup=kb_statistics)

