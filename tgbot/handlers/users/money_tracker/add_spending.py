import logging

from aiogram import types, F, Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.utils.formatting import as_list, Italic

from tgbot.states import MainMenuStates, MoneyTrackerStates
from tgbot.misc.callback_data import MoneyTrackerCallbackData, CommonCallbackData

from tgbot.keyboards import kb_main_menu, kb_back
from tgbot.keyboards.money_tracker_keyboards import kb_money_tracker_menu
from tgbot.utils import Database, ScreenManager


add_spending_router = Router(name=__name__)


@add_spending_router.callback_query(F.data == MoneyTrackerCallbackData.BACK.value,
                                    StateFilter(MoneyTrackerStates.choose_spending_type))
async def cancel_choosing_spending_type(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MoneyTrackerStates.choosing_service)
    await callback.message.edit_text(**ScreenManager.MONEY_TRACKER_MENU.as_kwargs())
    


@add_spending_router.callback_query(F.data,
                                    StateFilter(MoneyTrackerStates.choose_spending_type))
async def choosing_spending_type(callback: types. CallbackQuery, state: FSMContext):
    try:
        spending_type_id = int(callback.data)
        await state.update_data({"spending_type_id": spending_type_id})
        await state.set_state(MoneyTrackerStates.add_spending)
        await callback.message.edit_text(**ScreenManager.ENTER_SPENDING.as_kwargs())
    except Exception:
        pass


@add_spending_router.message(F.text, 
                             StateFilter(MoneyTrackerStates.add_spending))
async def add_spending(message: types.Message, state: FSMContext, db: Database, bot: Bot):
    state_data = await state.get_data()
    menu_message_id : Message = state_data.get("message_id")
    spending_type_id : int = state_data.get("spending_type_id")
    was_non_valid_input : bool = state_data.get("was_non_valid_input")

    user_spending = message.text
    try:
        user_spending = float(user_spending.replace(",", "."))
        if user_spending < 0: raise Exception
        db.add_spending(user_id=message.from_user.id, spending_type_id=spending_type_id, spending=user_spending)
        logging.info(f"User: {message.from_user.full_name} added spending {user_spending}")

        text = [
            "<b>Отслеживание трат</b>\n"
            f"<i>Трата <u>{user_spending}</u> успешно добавлена!</i>"
        ]
        await state.set_state(MoneyTrackerStates.choosing_service)
        await bot.edit_message_text(chat_id=message.chat.id, message_id=menu_message_id, text="\n".join(text), reply_markup=kb_money_tracker_menu)
    except:
        if not was_non_valid_input:
            await bot.edit_message_text(chat_id=message.chat.id, 
                                        message_id=menu_message_id, 
                                        **ScreenManager.ENTER_SPENDING_INVALID.as_kwargs())
            await state.update_data({"was_non_valid_input": True})
    finally:
        await message.delete()


@add_spending_router.callback_query(F.data == CommonCallbackData.BACK.value,
                                    StateFilter(MoneyTrackerStates.add_spending))
async def cancel_adding_spending(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(MoneyTrackerStates.choosing_service)
    await callback.message.edit_text(**ScreenManager.MONEY_TRACKER_MENU.as_kwargs())
