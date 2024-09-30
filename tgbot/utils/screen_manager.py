import logging

from aiogram.types import InlineKeyboardMarkup, Message

from tgbot.utils import Database

from tgbot.keyboards import *
from tgbot.keyboards.main_menu_kb import main_menu_kb
from tgbot.keyboards.money_tracker.edit_spending_types_kb import build_spending_types_for_edit_kb, edit_spending_type_kb
from tgbot.keyboards.money_tracker.spending_types_kb import build_spending_types_kb
from tgbot.keyboards.money_tracker.menu_kb import money_tracker_menu_kb
from tgbot.keyboards.money_tracker.statistics_kb import statistics_kb
from tgbot.keyboards.money_tracker.settings_menu_kb import settings_menu_kb


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

# TODO: Сделать крутой вывод, чтобы пользователь не мог фигню всякую ввести и сломать все нафиг
def editing_spending_type_text(user_id: int, type_id: int):
    type_name = Database.get_spending_type_name(user_id=user_id, type_id=type_id)
    text = [
        "Редактирование типа:",
        f"{type_name}\n",
        "Выберите:",
        "✏️ - изменить",
        "❌ - удалить",
    ]
    return "\n".join(text)


class ScreenManager:

    START_SCREEN = Screen(
        text="Добро пожаловать в бота по отслеживанию различных приколов. Выберите прикол для отслеживания:",
        reply_markup=main_menu_kb
        )
    
    # --- Money tracker screens --- #

    MONEY_TRACKER_MENU = Screen(
        text="<b>Отслеживание трат</b>\n\nВыберите нужное:",
        reply_markup=money_tracker_menu_kb
    )

    SPENDING_TYPE_CHOOSING = Screen(
        text="Выберите тип траты:",
        reply_markup=build_spending_types_kb
    )

    SPENDING_SUCCSESSFUL_ADDED = Screen(
        text=spending_successful_added_text,
        reply_markup=money_tracker_menu_kb
    )

    ENTER_SPENDING = Screen(
        text="Введите вашу трату:",
        reply_markup=back_kb
    )

    ENTER_SPENDING_INVALID = Screen(
        text="<b>Трата должна быть целым или десятичным положительным числом!</b>\n\nВведите размер траты:",
        reply_markup=back_kb
    )

    SETTINGS_MENU = Screen(
        text="Выберите настройку:",
        reply_markup=settings_menu_kb
    )

    SETTINGS_EDIT_SPENDING_TYPES_LIST = Screen(
        text="Выберие тип для изменения:",
        reply_markup=build_spending_types_for_edit_kb
    )

    SHOW_STATISTICS = Screen(
        text=show_statistics_text,
        reply_markup=statistics_kb
    )

    EDITING_SPENDING_TYPE = Screen(
        text=editing_spending_type_text,
        reply_markup=edit_spending_type_kb
    )

    ENTER_NEW_SPENDING_TYPE = Screen(
        text="Введите новый тип трат:",
        reply_markup=back_kb
    )

    NEW_SPENDING_TYPE_ADDED = Screen(
        text="<b>Новый тип трат добавлен</b>\n\nВыберите настройку:",
        reply_markup=settings_menu_kb
    )

    SPENDING_TYPE_DELETED = Screen(
        text="<b>Выбранный тип удален</b>\n\nВыберите настройку:",
        reply_markup=settings_menu_kb
    )

    EDIT_SPENDING_TYPE_NAME = Screen(
        text="Введите новое имя типа:",
        reply_markup=back_kb
    )

    SPENDING_TYPE_NAME_EDITED = Screen(
        text="<b>Тип трат изменен</b>\n\nВыберите настройку:",
        reply_markup=settings_menu_kb
    )
