from aiogram.types import Message
from aiogram.filters import Filter


class ValidSpendingFilter(Filter):

    async def __call__(self, message: Message):
        spending = message.text.split(" ")
        try:
            return float(spending[0].replace(",", ".")) > 0
        except:
            return False