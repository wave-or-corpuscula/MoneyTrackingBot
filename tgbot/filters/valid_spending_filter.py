from aiogram.types import Message
from aiogram.filters import Filter

from tgbot.config import Config
from tgbot.utils import Database


class ValidSpendingFilter(Filter):

    async def __call__(self, message: Message):
        spending = message.text.split(" ")
        try:
            float(spending[0].replace(",", "."))
            return True
        except:
            return False