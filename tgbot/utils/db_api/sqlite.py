import logging

from peewee import fn, ModelSelect

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
        # TODO: Сделать все траты удаленного типа типа Другое
        try:
            SpendingType.delete().where(SpendingType.id == type_id).execute()
            logging.info(f"DB Spending type with id: {type_id} deleted")
        except Exception as e:
            logging.error(f"Error while deleting type id {type_id}. \nError: {e}")
    
    def update_spending_type(self, type_id: int, new_name: str):
        try:
            SpendingType.update({SpendingType.type_name: new_name}).where(SpendingType.id == type_id).execute()
            logging.info(f"DB Spending type with id: {type_id} updated to {new_name}")
        except Exception as e:
            logging.error(f"Error while updating type id {type_id}. \nError: {e}")

