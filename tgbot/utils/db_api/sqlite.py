import peewee
import logging
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
