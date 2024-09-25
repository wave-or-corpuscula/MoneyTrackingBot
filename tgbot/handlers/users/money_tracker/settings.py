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
from tgbot.utils import Database


settings_router = Router(name=__name__)


# @settings_router.callback_query()