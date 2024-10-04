from aiogram.types import Message 
from aiogram.filters import Filter


class ValidIntegerFilter(Filter):

    def __init__(self, positive: bool = False):
        self.positive = positive

    async def __call__(self, message: Message) -> bool:
        try:
            return (not self.positive) or (int(message.text) > 0)
        except:
            return False
        