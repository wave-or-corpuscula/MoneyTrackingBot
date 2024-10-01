from aiogram import types, F, Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.utils.formatting import as_list, Italic

from tgbot.utils import Database, ScreenManager, Multitool
from tgbot.states import MainMenuStates
from tgbot.keyboards.main_menu_kb import MainMenuActions, MainMenuCbData


habits_tracker_router = Router(name=__name__)


