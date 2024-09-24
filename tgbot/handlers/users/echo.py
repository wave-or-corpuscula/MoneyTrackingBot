from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command, StateFilter

from tgbot.states import MainMenuState


echo_router = Router(name=__name__)

@echo_router.message(StateFilter(None))
async def bot_echo(message: Message, state: FSMContext):
    text = [
        "<i>Эхо без состояния</i>",
        "Сообщение:",
        message.text
    ]
    await state.set_state(MainMenuState.finance_controller)
    await message.answer("\n".join(text))


@echo_router.message(StateFilter("*"))
async def bot_echo_all(message: Message, state: FSMContext):
    text = [
        "<i>Эхо с состоянием</i>",
        f"Сообщение: {message.text}",
        f"Состояние: {await state.get_state()}",
    ]
    await message.answer("\n".join(text))