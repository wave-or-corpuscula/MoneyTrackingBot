import logging

from aiogram.types import InlineKeyboardMarkup, Message

from tgbot.utils import Database
from tgbot.keyboards import *
from tgbot.keyboards.money_tracker.spending_types_kb import build_spending_types_kb


class Screen:

    def __init__(self, text: str, reply_markup: InlineKeyboardMarkup | None):
        self.text = text
        self.reply_markup = reply_markup

    def as_kwargs(self, **kwargs):
        reply_markup = self.reply_markup(**kwargs) if callable(self.reply_markup) else self.reply_markup
        text = self.text(**kwargs) if callable(self.text) else self.text
        return {"text": text, "reply_markup": reply_markup}


def show_statistics_text(user_id: int, db: Database):
    week_spend = db.get_week_spending(user_id)
    month_spend = db.get_month_spending(user_id)
    text = [
        "<b>Статистика</b>\n",
        f"<i>Траты за месяц: <u>{month_spend}</u></i>",
        f"<i>Траты за неделю: <u>{week_spend}</u></i>",
    ]
    return "\n".join(text)


def spending_successful_added_text(user_spending: str,  spending_type_id: int, message: Message, db: Database):
    user_spending = float(user_spending.replace(",", "."))
    if user_spending < 0: raise Exception
    db.add_spending(user_id=message.from_user.id, spending_type_id=spending_type_id, spending=user_spending)
    logging.info(f"User: {message.from_user.full_name} added spending {user_spending}")

    text = [
        "<b>Отслеживание трат</b>\n",
        f"<i>Трата <u>{user_spending}</u> успешно добавлена!</i>"
    ]

    return "\n".join(text)


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

    SPENDING_SUCCSESSFUL_ADDED = Screen(
        text=spending_successful_added_text,
        reply_markup=kb_money_tracker_menu
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

    SETTINGS_EDIT_SPENDING_TYPES = Screen(
        text="Выберие действие:\n✏️ - изменить\n❌ - удалить",
        reply_markup=build_spending_types_kb
    )

    SHOW_STATISTICS = Screen(
        text=show_statistics_text,
        reply_markup=kb_statistics
    )