import logging

from aiogram import types, F, Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.enums.content_type import ContentType

from tgbot.states import MoneyTrackerStates
from tgbot.filters import ValidSpendingFilter
from tgbot.misc.callback_data.navigation import NavigationCbData, NavigationActions

from tgbot.utils import Database, ScreenManager
from tgbot.keyboards.money_tracker.spending_types_kb import SpendingTypesCbData
from tgbot.keyboards.money_tracker.menu_kb import MoneyTrackerMenuActions, MoneyTrackerMenuCbData

from tgbot.middlewares import DescriptionExtractMiddleware
from tgbot.filters import ZeroSpendingTypesFilter


add_spending_router = Router(name=__name__)

add_spending_router.message.middleware(DescriptionExtractMiddleware())


# --- Нет типов трат --- #

@add_spending_router.callback_query(
        MoneyTrackerMenuCbData.filter(F.action == MoneyTrackerMenuActions.add_spending),
        StateFilter(MoneyTrackerStates.choosing_service),
        ZeroSpendingTypesFilter()
)
async def no_spending_types_avaliable(callback: types.CallbackQuery):
    await callback.answer(**ScreenManager.NO_SPENDING_TYPES_AVALIABLE.as_kwargs(), show_alert=True)

# --- Нет типов трат --- #

# --- Выбор добавления новой траты --- #

@add_spending_router.callback_query(
        MoneyTrackerMenuCbData.filter(F.action == MoneyTrackerMenuActions.add_spending),
        StateFilter(MoneyTrackerStates.choosing_service)
)
async def add_spending_script(callback: types.CallbackQuery, state: FSMContext):
    await state.set_data({"chat_id": callback.message.chat.id, "message_id": callback.message.message_id})
    await state.set_state(MoneyTrackerStates.choose_spending_type)
    await callback.message.edit_text(**ScreenManager.SPENDING_TYPE_CHOOSING.as_kwargs(user_id=callback.from_user.id))

# --- Выбор добавления новой траты --- #


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
    except Exception as e:
        logging.error(e)

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


# --- Добавление траты --- #

@add_spending_router.message(
        F.content_type == ContentType.TEXT,
        StateFilter(MoneyTrackerStates.add_spending),
        ValidSpendingFilter()
)
async def add_spending(message: types.Message, state: FSMContext, db: Database, bot: Bot, spending: float, description: str | None):
    state_data = await state.get_data()
    menu_message_id : int = state_data.get("message_id")
    spending_type_id : int = state_data.get("spending_type_id")
    message.from_user
    db.add_spending(user_id=message.from_user.id, spending_type_id=spending_type_id, spending=spending, description=description)
    await state.set_state(MoneyTrackerStates.choosing_service)
    await bot.edit_message_text(chat_id=message.chat.id,
                                message_id=menu_message_id,
                                **ScreenManager.SPENDING_SUCCSESSFUL_ADDED.as_kwargs(spending=spending))
    await message.delete()

# --- Добавление траты --- #


# --- Невалидный ввод траты --- #

@add_spending_router.message(
        F.content_type == ContentType.TEXT,
        StateFilter(MoneyTrackerStates.add_spending),
)
async def invalid_spending(message: types.Message, state: FSMContext, bot: Bot):
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

# TODO: Сделать шорткат на ввод (из главного меню введенное числа воспринимается, как трата(та))
