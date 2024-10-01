import datetime

from peewee import (
    Model, IntegerField, FloatField, CharField, DateTimeField, ForeignKeyField
)
from playhouse.sqlite_ext import SqliteExtDatabase

from tgbot.config import load_config

config = load_config(".env")

# Создание базы данных SQLite
db = SqliteExtDatabase(config.db.database)

# Определение моделей
class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    id = IntegerField(primary_key=True)
    full_name = CharField()
    join_date = DateTimeField(default=datetime.datetime.now)

class SpendingType(BaseModel):
    id = IntegerField(primary_key=True)
    user_id = ForeignKeyField(User, backref='spending_types', on_delete='CASCADE', on_update='CASCADE')
    type_name = CharField()

class Spending(BaseModel):
    id = IntegerField(primary_key=True)
    user_id = ForeignKeyField(User, backref='spendings', on_delete='CASCADE', on_update='CASCADE')
    spending_type_id = ForeignKeyField(SpendingType, backref='spendings', on_delete='CASCADE', on_update='CASCADE')
    spending = FloatField()
    description = CharField(null=True, default=None)
    spending_date = DateTimeField(default=datetime.datetime.now)
