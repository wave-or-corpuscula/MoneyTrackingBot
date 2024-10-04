import logging

from typing import overload

from aiogram import types, F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.utils.formatting import as_list, Italic

from tgbot.filters import ValidIntegerFilter
from tgbot.utils import ScreenManager, Database
from tgbot.states import MoneyTrackerStates
from tgbot.misc.callback_data.navigation import NavigationActions, NavigationCbData
from tgbot.keyboards.money_tracker.spendings_pagination_kb import PaginationActions, PaginationCbData


spendings_pagination_router = Router(name=__name__)


@spendings_pagination_router.callback_query(
    NavigationCbData.filter(F.navigation == NavigationActions.back),
    StateFilter(MoneyTrackerStates.spendings_pagination)
)
async def cancel_spendings_pagination(callback: CallbackQuery, state: FSMContext):
    await state.set_state(MoneyTrackerStates.choosing_setting)
    await callback.message.edit_text(**ScreenManager.SETTINGS_MENU.as_kwargs())


# --- Навигация по тратам --- #

@spendings_pagination_router.callback_query(
    PaginationCbData.filter(F.action == PaginationActions.next),
    StateFilter(MoneyTrackerStates.spendings_pagination)
)
async def next_spending(callback: CallbackQuery, state: FSMContext):
    await offset_spendings(1, state, callback.message)


@spendings_pagination_router.callback_query(
    PaginationCbData.filter(F.action == PaginationActions.previous),
    StateFilter(MoneyTrackerStates.spendings_pagination)
)
async def previous_spending(callback: CallbackQuery, state: FSMContext):
    await offset_spendings(-1, state, callback.message)


@spendings_pagination_router.callback_query(
    PaginationCbData.filter(F.action == PaginationActions.goto),
    StateFilter(MoneyTrackerStates.spendings_pagination)
)
async def goto_spending_option(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    spendings_amount = len(state_data.get("spending_ids"))

    await state.update_data({"spending_message_id": callback.message.message_id})
    await state.set_state(MoneyTrackerStates.enter_spending_page)
    await callback.message.edit_text(**ScreenManager.ENTER_GOTO_PAGE.as_kwargs(spendings_amount=spendings_amount))


# Отмена

@spendings_pagination_router.callback_query(
    NavigationCbData.filter(F.navigation == NavigationActions.back),
    StateFilter(MoneyTrackerStates.enter_spending_page)
)
async def cancel_goto_spending(callback: CallbackQuery, state: FSMContext):
    await state.set_state(MoneyTrackerStates.spendings_pagination)
    await offset_spendings(0, state, callback.message)


@spendings_pagination_router.message(
    StateFilter(MoneyTrackerStates.enter_spending_page),
    ValidIntegerFilter(positive=True)
)
async def entered_goto_spending(message: Message, state: FSMContext, bot: Bot):
    state_data = await state.get_data()
    spending_ids = state_data.get("spending_ids")
    message_id = state_data.get("spending_message_id")
    goto_element_number = int(message.text)
    if goto_element_number <= len(spending_ids):
        await goto_spending_by_id(chat_id=message.chat.id, message_id=message_id, bot=bot, spending_ids=spending_ids, cur_index=goto_element_number - 1)
    # TODO: Обработать большой индекс
    await message.delete()


# --- Навигация по тратам --- #




async def offset_spendings(offset: int, state: FSMContext, message: Message):
    state_data = await state.get_data()
    cur_index = state_data.get("current_index")
    spending_ids = state_data.get("spending_ids")

    next_index = (offset + cur_index) % len(spending_ids)

    await state.update_data({"current_index": next_index})

    await goto_spending(message, spending_ids, next_index)


async def goto_spending(message: Message, spending_ids: list[int], cur_index: int):
    spending = Database.get_user_spending(spending_ids[cur_index])
    await message.edit_text(**ScreenManager.SPENDINGS_PAGINATION.as_kwargs(cur=cur_index + 1, total=len(spending_ids), spending=spending))

async def goto_spending_by_id(message_id: int, chat_id: int, bot: Bot, spending_ids: list[int], cur_index: int):
    spending = Database.get_user_spending(spending_ids[cur_index])
    await bot.edit_message_text(chat_id=chat_id, message_id=message_id, **ScreenManager.SPENDINGS_PAGINATION.as_kwargs(cur=cur_index + 1, total=len(spending_ids), spending=spending))
