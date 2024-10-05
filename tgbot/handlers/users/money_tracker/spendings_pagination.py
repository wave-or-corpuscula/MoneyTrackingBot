import logging

from aiogram import types, F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.utils.formatting import as_list, Italic
from aiogram.enums.content_type import ContentType

from tgbot.models import Spending
from tgbot.filters import ValidIntegerFilter, ValidSpendingPriceFilter
from tgbot.utils import ScreenManager, Database
from tgbot.states import MoneyTrackerStates
from tgbot.misc.callback_data.navigation import NavigationActions, NavigationCbData
from tgbot.keyboards.money_tracker.spendings_pagination_kb import PaginationActions, PaginationCbData
from tgbot.keyboards.money_tracker.edit_spending_kb import EditSpendingActions, EditSpendingCbData


spendings_pagination_router = Router(name=__name__)


@spendings_pagination_router.callback_query(
    NavigationCbData.filter(F.navigation == NavigationActions.back),
    StateFilter(MoneyTrackerStates.spendings_pagination)
)
async def cancel_spendings_pagination(callback: CallbackQuery, state: FSMContext):
    await state.set_state(MoneyTrackerStates.choosing_setting)
    await callback.message.edit_text(**ScreenManager.SETTINGS_MENU.as_kwargs())


# --- Пагинация по тратам --- #

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
    F.content_type == ContentType.TEXT,
    StateFilter(MoneyTrackerStates.enter_spending_page),
    ValidIntegerFilter(positive=True)
)
async def entered_goto_spending(message: Message, state: FSMContext, bot: Bot):
    state_data = await state.get_data()
    spending_ids = state_data.get("spending_ids")
    message_id = state_data.get("spending_message_id")
    goto_element_number = int(message.text)
    if goto_element_number <= len(spending_ids):
        await state.set_state(MoneyTrackerStates.spendings_pagination)
        await goto_spending_by_id(chat_id=message.chat.id, 
                                  message_id=message_id, 
                                  bot=bot,
                                  state=state,
                                  spending_ids=spending_ids, 
                                  cur_index=goto_element_number - 1)
        await message.delete()
    else:
        await entered_invalid_goto_spending(message, state, bot)


@spendings_pagination_router.message(
    F.content_type == ContentType.TEXT,
    StateFilter(MoneyTrackerStates.enter_spending_page)
)
async def entered_invalid_goto_spending(message: Message, state: FSMContext, bot: Bot):
    state_data = await state.get_data()
    spending_len = len(state_data.get("spending_ids"))
    message_id = state_data.get("spending_message_id")
    try:
        await bot.edit_message_text(chat_id=message.chat.id, 
                                    message_id=message_id, 
                                    **ScreenManager.INVALID_ENTER_GOTO_PAGE.as_kwargs(spendings_amount=spending_len))
    finally:
        await message.delete()

# --- Пагинация по тратам --- #


# --- Удаление траты --- #

@spendings_pagination_router.callback_query(
    StateFilter(MoneyTrackerStates.spendings_pagination),
    PaginationCbData.filter(F.action == PaginationActions.delete)
)
async def delete_spending(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    cur_index = state_data.get("current_index")
    spending_ids : list[int] = state_data.get("spending_ids")
    Database.delete_user_spending(spending_ids[cur_index])
    spending_ids.pop(cur_index)
    await state.update_data({"spending_ids": spending_ids})
    await callback.answer("Трата удалена")
    await offset_spendings(-1, state, callback.message)

# --- Удаление траты --- #


# TODO: Изменение трат
# --- Изменение траты --- #

@spendings_pagination_router.callback_query(
    StateFilter(MoneyTrackerStates.spendings_pagination),
    PaginationCbData.filter(F.action == PaginationActions.edit)
)
async def spending_settings_menu_show(callback: CallbackQuery, state: FSMContext):
    await state.set_state(MoneyTrackerStates.editing_spending)
    spending = await get_cur_spending(state)
    await callback.message.edit_text(**ScreenManager.EDIT_SPENDING_OPTIONS.as_kwargs(spending=spending))


# Отмена
@spendings_pagination_router.callback_query(
    StateFilter(MoneyTrackerStates.editing_spending),
    NavigationCbData.filter(F.navigation == NavigationActions.back)
)
async def cancel_spending_edit(callback: CallbackQuery, state: FSMContext):
    await state.set_state(MoneyTrackerStates.spendings_pagination)
    await offset_spendings(0, state, callback.message)


# -- Ввод новой суммы -- #

@spendings_pagination_router.callback_query(
    StateFilter(MoneyTrackerStates.editing_spending),
    EditSpendingCbData.filter(F.action == EditSpendingActions.edit_spending_price)
)
async def edit_spending_option(callback: CallbackQuery, state: FSMContext):
    await state.update_data({"message_id": callback.message.message_id})
    await state.set_state(MoneyTrackerStates.enter_new_spending_price)
    await callback.message.edit_text(**ScreenManager.ENTER_EDIT_SPENDING_PRICE.as_kwargs())


@spendings_pagination_router.callback_query(
    StateFilter(MoneyTrackerStates.enter_new_spending_price),
    NavigationCbData.filter(F.navigation == NavigationActions.back)
)
async def cancel_edit_spending_option(callback: CallbackQuery, state: FSMContext):
    await spending_settings_menu_show(callback, state)


@spendings_pagination_router.message(
    F.content_type == ContentType.TEXT,
    StateFilter(MoneyTrackerStates.enter_new_spending_price),
    ValidSpendingPriceFilter()
)
async def enter_valid_spending_price(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    message_id = data.get("message_id")
    cur_index = data.get("current_index")
    spending_ids = data.get("spending_ids")

    new_price = round(float(message.text.replace(",", ".")), 2)
    Database.update_spending_price(spending_ids[cur_index], new_price)
    
    cur_spending = await get_cur_spending(state)
    await state.set_state(MoneyTrackerStates.editing_spending)
    await bot.edit_message_text(chat_id=message.chat.id, 
                                message_id=message_id, 
                                **ScreenManager.ENTER_VALID_SPENDING_PRICE.as_kwargs(spending=cur_spending))
    await message.delete()


@spendings_pagination_router.message(
    F.content_type == ContentType.TEXT,
    StateFilter(MoneyTrackerStates.enter_new_spending_price),
)
async def enter_invalid_spending_price(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    message_id = data.get("message_id")
    try:
        await bot.edit_message_text(chat_id=message.chat.id, 
                                    message_id=message_id, 
                                    **ScreenManager.ENTER_INVALID_SPENDING_PRICE.as_kwargs())
    finally:
        await message.delete()

# -- Ввод новой суммы -- #

# -- Ввод нового описания -- #

@spendings_pagination_router.callback_query(
    StateFilter(MoneyTrackerStates.editing_spending),
    EditSpendingCbData.filter(F.action == EditSpendingActions.edit_spending_description)
)
async def edit_description_option(callback: CallbackQuery, state: FSMContext):
    await state.set_state(MoneyTrackerStates.enter_new_description)
    await state.update_data({"message_id": callback.message.message_id})
    await callback.message.edit_text(**ScreenManager.ENTER_NEW_DESCRIPTION.as_kwargs())

# Отмена
@spendings_pagination_router.callback_query(
    StateFilter(MoneyTrackerStates.enter_new_description),
    NavigationCbData.filter(F.navigation == NavigationActions.back)
)
async def cancel_edit_description_option(callback: CallbackQuery, state: FSMContext):
    await spending_settings_menu_show(callback, state)

@spendings_pagination_router.message(
    F.content_type == ContentType.TEXT,
    StateFilter(MoneyTrackerStates.enter_new_description)
)
async def enter_new_description(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    message_id = data.get("message_id")
    cur_index = data.get("current_index")
    spending_ids = data.get("spending_ids")

    Database.update_spending_description(spending_ids[cur_index], message.text)
    
    cur_spending = await get_cur_spending(state)
    await state.set_state(MoneyTrackerStates.editing_spending)
    await bot.edit_message_text(chat_id=message.chat.id, 
                                message_id=message_id, 
                                **ScreenManager.ENTER_VALID_DESCRIPTION.as_kwargs(spending=cur_spending))
    await message.delete()



# -- Ввод нового описания -- #


# --- Изменение траты --- #


# TODO: Нормальный формат даты


async def offset_spendings(offset: int, state: FSMContext, message: Message):
    state_data = await state.get_data()
    cur_index = state_data.get("current_index")
    spending_ids = state_data.get("spending_ids")

    next_index = (offset + cur_index) % len(spending_ids)

    await state.update_data({"current_index": next_index})
    await goto_spending(message, spending_ids, next_index)


async def get_cur_spending(state: FSMContext) -> Spending:
    state_data = await state.get_data()
    cur_index = state_data.get("current_index")
    spending_ids = state_data.get("spending_ids")
    return Database.get_user_spending(spending_ids[cur_index])

async def goto_spending(message: Message, spending_ids: list[int], cur_index: int):
    spending = Database.get_user_spending(spending_ids[cur_index])
    await message.edit_text(**ScreenManager.SPENDINGS_PAGINATION.as_kwargs(cur=cur_index + 1, total=len(spending_ids), spending=spending))

async def goto_spending_by_id(message_id: int, chat_id: int, bot: Bot, state: FSMContext, spending_ids: list[int], cur_index: int):
    await state.update_data({"current_index": cur_index})
    spending = Database.get_user_spending(spending_ids[cur_index])
    await bot.edit_message_text(chat_id=chat_id, 
                                message_id=message_id, 
                                **ScreenManager.SPENDINGS_PAGINATION.as_kwargs(cur=cur_index + 1, total=len(spending_ids), spending=spending))
