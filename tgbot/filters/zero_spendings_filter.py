from aiogram.types import CallbackQuery, User
from aiogram.filters import Filter

from tgbot.utils import Database


class ZeroSpendingsFilter(Filter):

    async def __call__(self, callback: CallbackQuery) -> bool:
        spendings_amount = Database.get_user_spendings_amount(callback.from_user.id)
        return spendings_amount == 0