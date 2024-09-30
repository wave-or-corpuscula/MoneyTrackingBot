import logging

from aiogram import types, F, Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter

from tgbot.states import MainMenuStates, MoneyTrackerStates
from tgbot.misc.callback_data.navigation import NavigationCbData, NavigationActions

from tgbot.utils import Database, ScreenManager
from tgbot.keyboards.money_tracker.spending_types_kb import SpendingTypesCbData
from tgbot.keyboards.money_tracker.menu_kb import MoneyTrackerMenuActions, MoneyTrackerMenuCbData


add_spending_router = Router(name=__name__)


@add_spending_router.callback_query(
        NavigationCbData.filter(F.navigation == NavigationActions.back),
        StateFilter(MoneyTrackerStates.choose_spending_type)
)
async def cancel_choosing_spending_type(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MoneyTrackerStates.choosing_service)
    await callback.message.edit_text(**ScreenManager.MONEY_TRACKER_MENU.as_kwargs())


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


@add_spending_router.message(
        F.text, 
        StateFilter(MoneyTrackerStates.add_spending)
)
async def add_spending(message: types.Message, state: FSMContext, db: Database, bot: Bot):
    state_data = await state.get_data()
    menu_message_id : int = state_data.get("message_id")
    spending_type_id : int = state_data.get("spending_type_id")
    was_non_valid_input : bool = state_data.get("was_non_valid_input")

    user_spending = message.text
    # Сделать возможность добавить описание к трате. То есть пользователь вводит сначала трату, а после пробела(ов) - описние к ней
    try:
        await bot.edit_message_text(chat_id=message.chat.id,
                                    message_id=menu_message_id,
                                    **ScreenManager.SPENDING_SUCCSESSFUL_ADDED.as_kwargs(message=message,
                                                                                         user_spending=user_spending,
                                                                                         spending_type_id=spending_type_id,
                                                                                         db=db))
        await state.set_state(MoneyTrackerStates.choosing_service)
    except Exception as e:
        if not was_non_valid_input:
            await bot.edit_message_text(chat_id=message.chat.id, 
                                        message_id=menu_message_id, 
                                        **ScreenManager.ENTER_SPENDING_INVALID.as_kwargs())
            await state.update_data({"was_non_valid_input": True})
    finally:
        await message.delete()


@add_spending_router.callback_query(
        NavigationCbData.filter(F.navigation == NavigationActions.back),
        StateFilter(MoneyTrackerStates.add_spending)
)
async def cancel_adding_spending(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MoneyTrackerStates.choosing_service)
    await callback.message.edit_text(**ScreenManager.MONEY_TRACKER_MENU.as_kwargs())
