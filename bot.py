import asyncio

import logging

import nest_asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from tgbot.config import load_config
from tgbot.utils.db_api.sqlite import DataBase

from tgbot.handlers import routers


async def on_startup(dp: Dispatcher, db: DataBase):
    db.create_tables()

async def main():

    nest_asyncio.apply()
    logging.basicConfig(level=logging.INFO)
    config = load_config(".env")

    storage = MemoryStorage()
    bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=storage)
    db = DataBase(config)

    dp.include_routers(*routers)

    try:
        await on_startup(dp, db)
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped!")


