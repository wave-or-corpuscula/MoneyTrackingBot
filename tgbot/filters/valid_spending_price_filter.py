from aiogram.types import Message
from aiogram.filters import Filter


class ValidSpendingPriceFilter(Filter):

    async def __call__(self, message: Message) -> bool:
        try:
            return float(message.text.replace(",", ".")) > 0
        except:
            return False