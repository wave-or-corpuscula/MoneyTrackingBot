from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter


commands_router = Router(name=__name__)


@commands_router.message(Command("start"), StateFilter(None))
async def command_start(message: Message):
    await message.answer("По этой команде будет выдаваться сообщение с главной менюшкой")