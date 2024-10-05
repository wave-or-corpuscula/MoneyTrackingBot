import logging

from aiogram.types import InlineKeyboardMarkup, Message
from aiogram.utils.formatting import Text, Underline

from tgbot.utils import Database

from tgbot.models import Spending

from tgbot.keyboards import *
from tgbot.keyboards.money_tracker.edit_spending_types_kb import build_spending_types_for_edit_kb, edit_spending_type_kb
from tgbot.keyboards.money_tracker.spending_types_kb import build_spending_types_kb
from tgbot.keyboards.money_tracker.menu_kb import money_tracker_menu_kb
from tgbot.keyboards.money_tracker.statistics_kb import statistics_kb
from tgbot.keyboards.money_tracker.settings_menu_kb import settings_menu_kb
from tgbot.keyboards.money_tracker.confirm_deleting_kb import confirm_deleting_kb
from tgbot.keyboards.money_tracker.spendings_pagination_kb import spendings_pagination_kb
from tgbot.keyboards.money_tracker.edit_spending_kb import edit_spending_kb


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
        "<b>Отслеживание трат</b>\n<i>Трата <u>{user_spending}</u> успешно добавлена!</i>"
    ]

    return "\n".join(text)

def editing_spending_type_text(user_id: int, type_id: int):
    type_name = Database.get_spending_type_name(user_id=user_id, type_id=type_id)
    underline_type_name = Text(Underline(type_name)).as_html()
    text = [
        f"Тип: {underline_type_name}\n",
        "Выберите:",
        "✏️ - изменить имя типа",
        "❌ - удалить",
    ]
    return "\n".join(text)


def about_text():
    return """
Данный бот создан для отслеживания своих финансовых трат.

<i>Тратой</i> я называю уменьшение личного капитала в связи с преобретением каких-либо благ (сам понял, что сказал?).
<i>Категория</i> траты - это обобщенная область, под которую можно подвести данную трату.

В пункте меню <b>Статистика</b> можно посмотреть траты за текущие месяц и неделю. Если вы хотите получить отчет за все время, выберите пункт <b>Полный отчет</b>.

По вопросам и предложениям можно обращаться к @wave_or_corpuscula
"""

def spendings_page_text(cur: int, total: int, spending: Spending):
    content = [
        f"<b>Трата: {cur} из {total}</b>",
        f"<i>Категория:</i> {spending.spending_type_id.type_name}",
        f"<i>Дата: {spending.spending_date}</i>\n",
        f"<u>Сумма</u>: {spending.spending}",
    ]

    if spending.description:
        desc = Text(spending.description).as_html()
        content.append(f"<u>Описание</u>: {desc}")
    return "\n".join(content)

def edit_spending_text(spending: Spending):
    content = [
        "<b>Трата:</b>\n",
        f"<b>Категория:</b> {spending.spending_type_id.type_name}",
        f"<i>Дата: {spending.spending_date}</i>\n",
        f"<b>Сумма</b>: <u>{spending.spending}</u>",
    ]

    if spending.description:
        desc = Text(spending.description).as_html()
        content.append(f"<b>Описание:</b> <u>{desc}</u>")
    content.append("\n<i>Выберите параметр для изменения:</i>")
    return "\n".join(content)


def enter_valid_spending_price_text(spending: Spending):
    return "<b>Сумма изменена</b>\n" + edit_spending_text(spending)


def enter_valid_spending_description_text(spending: Spending):
    return "<b>Описание изменено</b>\n" + edit_spending_text(spending)

def enter_valid_spending_spending_type_text(spending: Spending):
    return "<b>Категория изменена</b>\n" + edit_spending_text(spending)

class ScreenManager:
    
    # --- Money tracker screens --- #

    MONEY_TRACKER_MENU = Screen(
        text="<b>Отслеживание трат</b>\n\nВыберите нужное:",
        reply_markup=money_tracker_menu_kb
    )

    SHOW_ABOUT = Screen(
        text=about_text(),
        reply_markup=back_kb
    )

    SPENDING_TYPE_CHOOSING = Screen(
        text="Выберите категорию траты:",
        reply_markup=build_spending_types_kb
    )

    SPENDING_SUCCSESSFUL_ADDED = Screen(
        text=lambda spending: f"<i>Трата <u>{spending}</u> успешно добавлена!</i>\n\n<b>Отслеживание трат</b>",
        reply_markup=money_tracker_menu_kb
    )

    ENTER_SPENDING = Screen(
        text="<u>Формат ввода траты:</u>\n<i>10.99 [описание] (необязательно)</i>\n\nВведите вашу трату:",
        reply_markup=back_kb
    )

    ENTER_SPENDING_INVALID = Screen(
        text="<b>Трата должна быть десятичным положительным числом!</b>\n<i>После траты через пробел так же можете ввести ее описание</i>\n\nВведите размер траты:",
        reply_markup=back_kb
    )

    SETTINGS_MENU = Screen(
        text="Выберите настройку:",
        reply_markup=settings_menu_kb
    )

    SETTINGS_EDIT_SPENDING_TYPES_LIST = Screen(
        text="Выберие категорию для изменения:",
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
        text="Введите называние новой категории:",
        reply_markup=back_kb
    )

    ENTER_INVALID_SPENDING_TYPE = Screen(
        text=lambda max_len: f"<b>Длина должна быть меньше {max_len} символов</b>\n<i>Некоторые emoji занимают 2 символа</i>\n\nВведите название типа трат:",
        reply_markup=back_kb
    )

    NEW_SPENDING_TYPE_ADDED = Screen(
        text="<b>Новая категория добавлена</b>\n\nВыберие категорию для изменения:",
        reply_markup=build_spending_types_for_edit_kb
    )

    SPENDING_TYPE_DELETED = Screen(
        text="<b>Выбранная категория удалена</b>\n\nВыберие категорию для изменения:",
        reply_markup=build_spending_types_for_edit_kb
    )

    EDIT_SPENDING_TYPE_NAME = Screen(
        text="Введите новое имя типа:",
        reply_markup=back_kb
    )

    SPENDING_TYPE_NAME_EDITED = Screen(
        text="<b>Категория изменена</b>\n\nВыберие категорию для изменения:",
        reply_markup=build_spending_types_for_edit_kb
    )

    CONFIRM_DELETING_SPENDING_TYPE = Screen(
        text="Вы точно хотите удалить выбранный тип?\n\n<b><u>Все траты этого типа будут удалены</u></b>",
        reply_markup=confirm_deleting_kb
    )

    MAX_SPENDING_TYPES_ALERT = Screen(
        text=lambda max_types : f"Максимальное количество типов трат - {max_types}",
        reply_markup=None
    )

    REPORT_FORMING = Screen(
        text="Формирование отчета...",
        reply_markup=None
    )

    NO_SPENDING_TYPES_AVALIABLE = Screen(
        text="Вы не можете добавить новую трату, так как у вас нет типов трат!\n\nДля добавления типа траты перейдите в \nНастойки->Изменить типы трат->Новый тип",
        reply_markup=None
    )

    SPENDINGS_PAGINATION = Screen(
        text=spendings_page_text,
        reply_markup=spendings_pagination_kb
    )

    ENTER_GOTO_PAGE = Screen(
        text=lambda spendings_amount: f"Введите номер траты\n<i>Между 1 и {spendings_amount}</i>:",
        reply_markup=back_kb
    )

    INVALID_ENTER_GOTO_PAGE = Screen(
        text=lambda spendings_amount: f"<b><u>Число должно быть между 1 и {spendings_amount}</u></b>\n\nВведите номер траты:",
        reply_markup=back_kb
    )

    EDIT_SPENDING_OPTIONS = Screen(
        text=edit_spending_text,
        reply_markup=edit_spending_kb
    )

    ENTER_EDIT_SPENDING_PRICE = Screen(
        text="Введите новую сумму:",
        reply_markup=back_kb
    )

    ENTER_VALID_SPENDING_PRICE = Screen(
        text=enter_valid_spending_price_text,
        reply_markup=edit_spending_kb
    )

    ENTER_INVALID_SPENDING_PRICE = Screen(
        text="<b>Трата должна быть десятичным положительным числом!</b>\nВведите новую сумму:",
        reply_markup=back_kb
    )

    ENTER_NEW_DESCRIPTION = Screen(
        text="Введите новый текст описания:",
        reply_markup=back_kb
    )

    ENTER_VALID_DESCRIPTION = Screen(
        text=enter_valid_spending_description_text,
        reply_markup=edit_spending_kb
    )

    EDIT_SPENDING_SPENDING_TYPE = Screen(
        text="Выберите новую категорию для своей траты:", 
        reply_markup=build_spending_types_kb
    )

    ENTER_VALID_SPENDING_SPENDING_TYPE = Screen(
        text=enter_valid_spending_spending_type_text,
        reply_markup=edit_spending_kb
    )
