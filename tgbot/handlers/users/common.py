from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import Text, Bold, as_list, Italic

from tgbot.states import MainMenuStates
from tgbot.keyboards import kb_main_menu
from tgbot.utils import Database


common_router = Router(name=__name__)


@common_router.message(Command("start"), StateFilter(None))
async def command_start(message: Message, state: FSMContext, db: Database):
    db.add_user(message.from_user.id, message.from_user.full_name)
    await state.set_state(MainMenuStates.choosing_service)
    await message.answer("Добро пожаловать в бота по отслеживанию различных приколов. Выберите прикол для отслеживания:",
                         reply_markup=kb_main_menu)

# Продвинутое решение работы с пользовательским именем (ни и вообще, если нужно вывести то, что ввел пользователь)
@common_router.message(Command("hello"), StateFilter("*"))
async def greet_user(message: Message):
    content = Text(
        "Здравствуй, ",
        Bold(message.from_user.full_name),
        "!"
    )
    await message.answer(**content.as_kwargs())

# --- ECHO HANDLERS --- #

@common_router.message(StateFilter(None))
async def bot_echo(message: Message, state: FSMContext):
    content = as_list(
        Italic("Эхо без состояния"),
        "Сообщение:",
        message.text,
        sep="\n"
    )
    await message.answer(**content.as_kwargs())
    await message.delete()


@common_router.message(StateFilter("*"))
async def bot_echo_all(message: Message, state: FSMContext):
    content = as_list(
        Italic("Эхо с состоянием"),
        f"Сообщение: {message.text}",
        f"Состояние: {await state.get_state()}",
        sep="\n",
    )
    await message.answer(**content.as_kwargs())
    await message.delete()


@common_router.callback_query(StateFilter("*"))
async def callback_echo(callback: types.CallbackQuery, state: FSMContext):
    content = as_list(
        Italic("Необработыннй callback"),
        f"Данные: {callback.data}",
        f"Состояние: {await state.get_state()}",
        sep="\n",
    )
    # await callback.answer(f"")
    await callback.message.answer(**content.as_kwargs())
