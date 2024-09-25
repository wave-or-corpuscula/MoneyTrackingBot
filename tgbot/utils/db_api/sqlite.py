from peewee import fn

import logging

from datetime import datetime, timedelta

from playhouse.sqlite_ext import SqliteExtDatabase

from tgbot.config import Config
from tgbot.models import User, SpendingType, Spending


class Database:

    def __init__(self, config: Config):
        self.db = SqliteExtDatabase(config.db.database)

    def create_tables(self):
        self.db.connect()
        self.db.create_tables([User, SpendingType, Spending])
        self.db.close()
    
    def add_user(self, user_id: int, full_name: str):
        try:
            User.create(id=user_id, full_name=full_name)
            logging.info(f"DB User: {full_name} with id: {user_id} created")
        except Exception as e:
            logging.error(f"Error adding user {full_name}, id {user_id}. \nError: {e}")
        
    def add_spending(self, user_id: int, spending_type_id: int, spending: float):
        try:
            Spending.create(user_id=user_id, spending_type_id=spending_type_id, spending=spending)
            logging.info(f"DB spending for user {user_id} created")
        except Exception as e:
            logging.error(f"Cannot create spending {spending} for user {user_id}. \nError: {e}")

    def get_week_spending(self, user_id: int):
        today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

        start_of_week = today - timedelta(days=today.weekday())

        sum_week = (Spending
                    .select(fn.SUM(Spending.spending))
                    .where(
                        (Spending.user_id == user_id) &
                        (Spending.spending_date >= start_of_week) &
                        (Spending.spending_date <= today)
                    )
                    .scalar())
        return sum_week

    def get_month_spending(self, user_id: int):
        today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        start_of_month = today.replace(day=1)

        sum_month = (Spending
                    .select(fn.SUM(Spending.spending))
                    .where(
                        (Spending.user_id == user_id) &  
                        (Spending.spending_date >= start_of_month) &
                        (Spending.spending_date <= today)
                    )
                    .scalar())
        return sum_month
