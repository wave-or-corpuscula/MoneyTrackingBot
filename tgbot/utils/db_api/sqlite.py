from peewee import fn

import logging

from datetime import datetime, timedelta

from playhouse.sqlite_ext import SqliteExtDatabase

from tgbot.config import Config
from tgbot.models import User, SpendingType, Spending


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
        
    def add_spending(self, user_id: int, spending_type_id: int, spending: float):
        try:
            Spending.create(user_id=user_id, spending_type_id=spending_type_id, spending=spending)
            logging.info(f"DB spending for user {user_id} created")
        except Exception as e:
            logging.error(f"Cannot create spending {spending} for user {user_id}. \nError: {e}")

    def _get_user_spending_in_bounds(self, user_id: int, start_date: datetime, end_date: datetime):
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
        return self._get_user_spending_in_bounds(user_id, start_of_week, today)

    def get_month_spending(self, user_id: int):
        today = datetime.today()
        start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return self._get_user_spending_in_bounds(user_id, start_of_month, today)
