from aiogram.types import CallbackQuery
from aiogram.filters import Filter

from tgbot.config import Config
from tgbot.utils import Database


class ZeroSpendingTypesFilter(Filter):

    async def __call__(self, callback: CallbackQuery) -> bool:
        user_spending_types = Database.get_user_spending_types_amount(user_id=callback.from_user.id)
        return user_spending_types == 0
