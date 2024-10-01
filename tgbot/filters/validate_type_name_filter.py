from aiogram.types import Message
from aiogram.filters import Filter

from tgbot.config import Config


class ValidateTypeNameFilter(Filter):

    def __init__(self):
        pass

    async def __call__(self, message: Message, config: Config) -> bool:
        return len(message.text) > config.bot_settings.max_spending_type_len