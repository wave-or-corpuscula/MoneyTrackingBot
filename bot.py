import asyncio

import logging

from redis import Redis

import nest_asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage

from tgbot.config import load_config
from tgbot.utils.db_api.sqlite import Database

from tgbot.handlers import routers


async def on_startup(dp: Dispatcher, db: Database):
    db.create_tables()


async def main():

    nest_asyncio.apply()
    logging.basicConfig(level=logging.INFO)
    config = load_config(".env")

    if config.tg_bot.use_redis:
        pass
        # storage = RedisStorage() # TODO: Reddis initialization
    else: 
        storage = MemoryStorage()
    bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=storage)
    db = Database(config)

    dp["db"] = db

    dp.include_routers(*routers)

    try:
        await on_startup(dp, db)
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped!")


