from aiogram.types import InlineKeyboardMarkup

from tgbot.keyboards import *


class Screen:

    def __init__(self, text: str, reply_markup: InlineKeyboardMarkup | None):
        self.text = text
        self.reply_markup = reply_markup

    def as_kwargs(self):
        if callable(self.reply_markup):
            self.reply_markup = self.reply_markup()
        return self.__dict__


class ScreenManager:

    START_SCREEN = Screen(
        text="Добро пожаловать в бота по отслеживанию различных приколов. Выберите прикол для отслеживания:",
        reply_markup=kb_main_menu
        )
    
    # --- Money tracker screens --- #

    MONEY_TRACKER_MENU = Screen(
        text="<b>Отслеживание трат</b>\n\nВыберите нужное:",
        reply_markup=kb_money_tracker_menu
    )

    SPENDING_TYPE_CHOOSING = Screen(
        text="Выберите тип траты:",
        reply_markup=kb_spending_types
    )

    ENTER_SPENDING = Screen(
        text="Введите вашу трату:",
        reply_markup=kb_back
    )

    ENTER_SPENDING_INVALID = Screen(
        text="<b>Трата должна быть целым или десятичным положительным числом!</b>\n\nВведите размер траты:",
        reply_markup=kb_back
    )

    SETTINGS_MENU = Screen(
        text="Выберите настройку:",
        reply_markup=kb_settings_menu
    )
