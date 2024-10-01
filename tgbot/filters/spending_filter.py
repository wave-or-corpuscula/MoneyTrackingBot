from aiogram.types import Message
from aiogram.filters import Filter

from tgbot.config import Config
from tgbot.utils import Database


class SpendingFilter(Filter):

    def __init__(self, with_description: bool) -> None:
        self.with_description = with_description

    async def __call__(self, message: Message):
        spending = message.text.split(" ")
        try:
            float(spending[0].replace(",", "."))
        except:
            return False
        return len(spending) > 1 == self.with_description