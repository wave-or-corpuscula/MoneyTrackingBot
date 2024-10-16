import sys

import locale

import logging

import calendar

from peewee import fn, ModelSelect

from datetime import datetime, timedelta, date

from playhouse.sqlite_ext import SqliteExtDatabase

from tgbot.config import Config
from tgbot.models import User, SpendingType, Spending


locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


class Database:

    def __init__(self, config: Config, default_spending_types: list):
        self.db = SqliteExtDatabase(config.db.database)
        self.default_spending_types = default_spending_types

    def create_tables(self):
        self.db.connect()
        self.db.create_tables([User, SpendingType, Spending])
        self.db.close()
    
    def _get_spending_types_rows(self, user_id: int):
        return [{"user_id": user_id, "type_name": type_name} for type_name in self.default_spending_types]

    def add_user(self, user_id: int, full_name: str):
        try:
            User.create(id=user_id, full_name=full_name)
            SpendingType.insert_many(self._get_spending_types_rows(user_id)).execute()
            logging.info(f"DB User: {full_name} with id: {user_id} created")
        except Exception as e:
            logging.error(f"Error adding user {full_name}, id {user_id}. \nError: {e}")
        
    def add_spending(self, user_id: int, spending_type_id: int, spending: float, description: str = None):
        try:
            Spending.create(user_id=user_id, spending_type_id=spending_type_id, spending=spending, description=description)
            logging.info(f"DB User: {user_id}, created spending: {spending} with text: {description}")
        except Exception as e:
            logging.error(f"Cannot create spending {spending} for user {user_id}. \nError: {e}")

    def _get_user_spendings_sum_in_bounds(self, user_id: int, start_date: datetime, end_date: datetime) -> float:
        bounds_spending = (Spending
                           .select(fn.SUM(Spending.spending))
                           .where(
                               (Spending.user_id == user_id) &
                               (Spending.spending_date >= start_date) &
                               (Spending.spending_date <= end_date)
                           )
                           .scalar())
        return round(bounds_spending, 2) if bounds_spending else 0

    def get_week_spending(self, user_id: int):
        today = datetime.today()
        start_of_week = (today - timedelta(days=today.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
        return self._get_user_spendings_sum_in_bounds(user_id, start_of_week, today)

    def get_month_spending(self, user_id: int):
        today = datetime.today()
        start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return self._get_user_spendings_sum_in_bounds(user_id, start_of_month, today)
    
    @staticmethod
    def get_user_spending_types(user_id: int) -> ModelSelect:
        return SpendingType.select().where((SpendingType.user_id == user_id))

    @staticmethod
    def get_spending_type_name(user_id: int, type_id: int) -> str:
        return (SpendingType
                .select(SpendingType.type_name)
                .where(SpendingType.user_id == user_id, SpendingType.id == type_id)
                .scalar())
    
    def add_spending_type(self, user_id: int, type_name: str):
        try:
            SpendingType.create(user_id=user_id, type_name=type_name)
            logging.info(f"DB User with id: {user_id} created new type: {type_name}")
        except Exception as e:
            logging.error(f"Error while adding new type user: {user_id}. \nError: {e}")

    def delete_spending_type(self, type_id: int):
        try:
            SpendingType.delete().where(SpendingType.id == type_id).execute()
            spendings_amount = Spending.delete().where(Spending.spending_type_id == type_id).execute()
            logging.info(f"DB Spending type with id: {type_id} with {spendings_amount} spendings deleted")
        except Exception as e:
            logging.error(f"Error while deleting type id {type_id}. \nError: {e}")
    
    def update_spending_type(self, type_id: int, new_name: str):
        try:
            SpendingType.update({SpendingType.type_name: new_name}).where(SpendingType.id == type_id).execute()
            logging.info(f"DB Spending type with id: {type_id} updated to {new_name}")
        except Exception as e:
            logging.error(f"Error while updating type id {type_id}. \nError: {e}")

    @staticmethod
    def get_user_spending_types_amount(user_id: int) -> int:
        return SpendingType.select().where(SpendingType.user_id == user_id).count()
    
    @staticmethod
    def get_user_spendings_amount(user_id: int) -> int:
        return Spending.select().where(Spending.user_id == user_id).count()

    # --- Получение трат пользователя для отчета --- #\

    def _get_user_spendings_in_bounds(self, user_id: int, start_date: datetime, end_date: datetime) -> list[Spending]:
        bounded_spendings = (Spending
                 .select()
                 .where(
                     (Spending.user_id == user_id) &
                     (Spending.spending_date > start_date) &
                     (Spending.spending_date < end_date)
                 ))
        return list(bounded_spendings)

    @staticmethod
    def get_user_spendings(user_id: int) -> list[Spending]:
        spendings : list[Spending] = (Spending.select(SpendingType.type_name, Spending.spending, Spending.description, Spending.spending_date)
                                      .where(Spending.user_id == user_id)
                                      .join(SpendingType, on=(Spending.spending_type_id == SpendingType.id)))
        return spendings
    
    def _get_user_month_spendings(self, user_id: int, year: int, month: int) -> list[Spending]:
        month_range = calendar.monthrange(year=year, month=month)
        start_date = datetime(year, month, month_range[0])
        end_date = datetime(year, month, month_range[1]) + timedelta(days=1)
        month_spendings = self._get_user_spendings_in_bounds(user_id, 
                                                            start_date=start_date,
                                                            end_date=end_date)
        return month_spendings
    
    def _get_spending_dates(self, user_id: int) -> list[datetime]:
        dates : list[Spending] = Spending.select(fn.strftime("%Y-%m", Spending.spending_date)).where(Spending.user_id == user_id).distinct()
        return [datetime.strptime(d.spending_date, "%Y-%m") for d in dates]

    def get_user_spendings_by_month(self, user_id: int) -> dict[str, list[Spending]]:
        spendings_dates = self._get_spending_dates(user_id)

        spendings_aggregation = {}
        for spend_date in spendings_dates:
            month_date = f"{spend_date.strftime("%B")} {spend_date.year}"
            month_spendings = self._get_user_month_spendings(user_id=user_id, year=spend_date.year, month=spend_date.month)
            spendings_aggregation[month_date] = month_spendings
        return spendings_aggregation

    # --- Получение трат пользователя для отчета --- #\

    @staticmethod
    def get_spendings_ids(user_id: int) -> list[int]:
        spendings = Spending.select(Spending.id).where(Spending.user_id == user_id)
        return [spending.id for spending in spendings]
    
    @staticmethod
    def get_user_spending(spending_id: int) -> Spending:
        return (Spending.select()
                .where(Spending.id == spending_id)
                .join(SpendingType, on=(Spending.spending_type_id == SpendingType.id)))[0]
    
    @staticmethod
    def delete_user_spending(spending_id: int) -> None:
        Spending.delete().where(Spending.id == spending_id).execute()

    @staticmethod
    def update_spending_price(spending_id: int, new_price: float):
        Spending.update({Spending.spending: new_price}).where(Spending.id == spending_id).execute()

    @staticmethod
    def update_spending_description(spending_id: int, new_description: str):
        Spending.update({Spending.description: new_description}).where(Spending.id == spending_id).execute()
        
    @staticmethod
    def update_spending_spending_type(spending_id: int, new_spending_type_id: str):
        logging.info(f"DB spending with id: {spending_id}, now has {new_spending_type_id} type")
        Spending.update({Spending.spending_type_id: new_spending_type_id}).where(Spending.id == spending_id).execute()

# TODO: Добавить логи из БД (БОЛЬШЕ ЛОГОВ, может, даже сделать отдельный логер для базы данных?????!!!!)