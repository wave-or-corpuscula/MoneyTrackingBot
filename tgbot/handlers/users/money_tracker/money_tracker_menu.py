from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter

from tgbot.states import MainMenuStates, MoneyTrackerMenuStates
from tgbot.misc.callback_data import MoneyTrackerCallbackData, CommonCallbackData

from tgbot.keyboards.money_tracker_keyboards import kb_money_tracker_menu


money_tracker_router = Router(name=__name__)


@money_tracker_router.callback_query(F.data == CommonCallbackData.MONEY_TRACKER, 
                                     StateFilter(MainMenuStates.choosing_service))
async def money_tracker_main_menu(callback: types.CallbackQuery, state: FSMContext):
    text = [
        "Вы выбрали: <b>Отслеживание трат</b>",
        "Выберите нужное:"
    ]
    await state.set_state(MoneyTrackerMenuStates.choosing_service)
    await callback.message.edit_text("\n".join(text), reply_markup=kb_money_tracker_menu)


