from aiogram import BaseMiddleware
from aiogram.types import Message

from typing import Callable, Dict, Awaitable, Any


class DescriptionExtractMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        try:
            spending_parts = event.text.split(" ")
            data["spending"] = round(float(spending_parts[0]), 2)
            description = " ".join(spending_parts[1:])
            data["description"] = None if len(description) == 0 else description
        finally:
            return await handler(event, data)
