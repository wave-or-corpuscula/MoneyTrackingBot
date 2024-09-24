from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter

from tgbot.states import MainMenuStates
from tgbot.keyboards import kb_main_menu


common_router = Router(name=__name__)


@common_router.message(Command("start"), StateFilter(None))
async def command_start(message: Message, state: FSMContext):

    await state.set_state(MainMenuStates.choosing_service)
    await message.answer("Добро пожаловать в бота по отслеживанию различных приколов. Выберите прикол для отслеживания:",
                         reply_markup=kb_main_menu)
    

@common_router.message(StateFilter(None))
async def bot_echo(message: Message, state: FSMContext):
    text = [
        "<i>Эхо без состояния</i>",
        "Сообщение:",
        message.text
    ]
    await state.set_state(MainMenuStates.finance_controller)
    await message.answer("\n".join(text))


@common_router.message(StateFilter("*"))
async def bot_echo_all(message: Message, state: FSMContext):
    text = [
        "<i>Эхо с состоянием</i>",
        f"Сообщение: {message.text}",
        f"Состояние: {await state.get_state()}",
    ]
    await message.answer("\n".join(text))