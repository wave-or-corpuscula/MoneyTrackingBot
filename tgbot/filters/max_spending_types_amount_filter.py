from aiogram.types import Message
from aiogram.filters import Filter

from tgbot.config import Config
from tgbot.utils import Database


class MaxSpendingTypesAmountFilter(Filter):

    def __init__(self) -> None:
        pass

    async def __call__(self, message: Message, config: Config) -> bool:
        types_amount = Database.get_user_spending_types_amount(message.from_user.id)
        return types_amount >= config.bot_settings.max_spending_types_amount
