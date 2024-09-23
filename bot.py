import asyncio

import nest_asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

# from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage

from tgbot.config import load_config
from tgbot.utils.db_api.sqlite import DataBase

from tgbot.handlers.users.echo import register_echo_handlers



async def on_startup(dp: Dispatcher, db: DataBase):
    db.create_tables()
    # await set_default_commands(dp)
    # await notify_admins(dp)

def register_handlers(dp: Dispatcher):
    register_echo_handlers(dp)


async def main():

    nest_asyncio.apply()

    config = load_config(".env")

    loop = asyncio.get_event_loop()

    storage = MemoryStorage()
    bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher(storage=storage, loop=loop)
    db = DataBase(config)

    bot.__setattr__("config", config)
    bot.__setattr__("db", db)

    register_handlers(dp)

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


