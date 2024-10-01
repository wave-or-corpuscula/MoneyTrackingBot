import logging

from aiogram import types, F, Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.enums.content_type import ContentType

from tgbot.states import MainMenuStates, MoneyTrackerStates
from tgbot.filters import SpendingFilter
from tgbot.misc.callback_data.navigation import NavigationCbData, NavigationActions

from tgbot.utils import Database, ScreenManager
from tgbot.keyboards.money_tracker.spending_types_kb import SpendingTypesCbData
from tgbot.keyboards.money_tracker.menu_kb import MoneyTrackerMenuActions, MoneyTrackerMenuCbData


add_spending_router = Router(name=__name__)


# --- Отмена добавления траты --- #

@add_spending_router.callback_query(
        NavigationCbData.filter(F.navigation == NavigationActions.back),
        StateFilter(MoneyTrackerStates.choose_spending_type)
)
async def cancel_choosing_spending_type(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MoneyTrackerStates.choosing_service)
    await callback.message.edit_text(**ScreenManager.MONEY_TRACKER_MENU.as_kwargs())


# --- Выбор типа траты --- #

@add_spending_router.callback_query(
        SpendingTypesCbData.filter(),
        StateFilter(MoneyTrackerStates.choose_spending_type)
)
async def choosing_spending_type(callback: types. CallbackQuery, callback_data: SpendingTypesCbData, state: FSMContext):
    try:
        await state.update_data({"spending_type_id": callback_data.type_id})
        await state.set_state(MoneyTrackerStates.add_spending)
        await callback.message.edit_text(**ScreenManager.ENTER_SPENDING.as_kwargs())
    except Exception:
        pass

# --- Выбор типа траты --- #


# --- Отмена выбора типа траты --- #

@add_spending_router.callback_query(
        NavigationCbData.filter(F.navigation == NavigationActions.back),
        StateFilter(MoneyTrackerStates.add_spending)
)
async def cancel_adding_spending(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MoneyTrackerStates.choosing_service)
    await callback.message.edit_text(**ScreenManager.MONEY_TRACKER_MENU.as_kwargs())

# --- Отмена выбора типа траты --- #


# --- Добавление траты с описанием --- #

@add_spending_router.message(
        F.content_type == ContentType.TEXT,
        SpendingFilter(with_description=True),
        StateFilter(MoneyTrackerStates.add_spending)
)
async def add_spending_with_description(message: types.Message, state: FSMContext, db: Database, bot: Bot):
    state_data = await state.get_data()
    menu_message_id : int = state_data.get("message_id")
    spending_type_id : int = state_data.get("spending_type_id")
    spending_parts = message.text.split(" ")
    spending = round(float(spending_parts[0]), 2)
    description = " ".join(spending_parts[1:])
    db.add_spending(user_id=message.from_user.id, spending_type_id=spending_type_id, spending=spending, description=description)
    await state.set_state(MoneyTrackerStates.choosing_service)
    await bot.edit_message_text(chat_id=message.chat.id,
                                message_id=menu_message_id,
                                **ScreenManager.SPENDING_SUCCSESSFUL_ADDED.as_kwargs(spending=spending))
    await message.delete()

# --- Добавление траты с описанием --- #


# --- Добавление траты без описания --- #

@add_spending_router.message(
        F.content_type == ContentType.TEXT,
        SpendingFilter(with_description=False),
        StateFilter(MoneyTrackerStates.add_spending)
)
async def add_spending_with_no_description(message: types.Message, state: FSMContext, db: Database, bot: Bot):
    state_data = await state.get_data()
    menu_message_id : int = state_data.get("message_id")
    spending_type_id : int = state_data.get("spending_type_id")
    spending = round(float(message.text), 2)
    db.add_spending(user_id=message.from_user.id, spending_type_id=spending_type_id, spending=spending)
    await state.set_state(MoneyTrackerStates.choosing_service)
    await bot.edit_message_text(chat_id=message.chat.id,
                                message_id=menu_message_id,
                                **ScreenManager.SPENDING_SUCCSESSFUL_ADDED.as_kwargs(spending=spending))
    await message.delete()

# --- Добавление траты без описания --- #


# --- Невалидный ввод траты --- #

@add_spending_router.message(
        F.content_type == ContentType.TEXT,
        StateFilter(MoneyTrackerStates.add_spending)
)
async def add_spending(message: types.Message, state: FSMContext, bot: Bot):
    state_data = await state.get_data()
    menu_message_id : int = state_data.get("message_id")
    was_non_valid_input : bool = state_data.get("was_non_valid_input")
    if not was_non_valid_input:
        await bot.edit_message_text(chat_id=message.chat.id, 
                                    message_id=menu_message_id, 
                                    **ScreenManager.ENTER_SPENDING_INVALID.as_kwargs())
        await state.update_data({"was_non_valid_input": True})
    await message.delete()

# --- Невалидный ввод траты --- #
