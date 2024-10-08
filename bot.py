import asyncio

import logging

import nest_asyncio

from redis import Redis

from aiohttp import web

from aiogram import Bot, Dispatcher, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage

from tgbot.config import Config, load_config
from tgbot.utils.db_api.sqlite import Database

from tgbot.handlers import routers


async def on_startup(dp: Dispatcher, db: Database):
    db.create_tables()


async def set_webhook(bot: Bot, webhook_path: str):
    webhook_url = f"https://8815-46-216-242-85.ngrok-free.app{webhook_path}"
    await bot.set_webhook(url=webhook_url)


async def on_startup_webhooks(bot: Bot, webhook_path: str, _):
    await set_webhook(bot, webhook_path)


async def handle_webhook(bot: Bot, dp: Dispatcher, BOT_TOKEN: str, request):
    url = str(request.url)
    index = url.rfind("/")
    token = url[index + 1:]

    if token == BOT_TOKEN:
        request_data = await request.json()
        update = types.Update(**request_data)
        await dp.feed_update(bot=bot, update=update)
        return web.Response()
    else:
        return web.Resource(status=403)


async def main():

    nest_asyncio.apply()
    logging.basicConfig(level=logging.INFO)
    config : Config = load_config(".env")

    if config.tg_bot.use_redis:
        pass# storage = RedisStorage.from_url("redis://localhost:6379/0")
    else: 
        storage = MemoryStorage()
    bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=storage)
    db = Database(config, default_spending_types=["🥦 Еда", "🎉 Развлечения", "💪 Здоровье", "🙈 Другое"])

    dp["db"] = db
    dp["config"] = config


    dp.include_routers(*routers)

    try:
        # Use webhooks
        if config.tg_bot.use_webhooks:
            app = web.Application()
            app.on_startup.append(lambda _: on_startup_webhooks(bot, webhook_path, _))
            webhook_path = f"/{config.tg_bot.token}"

            app.router.add_post(
                path=f"/{config.tg_bot.token}",
                handler=lambda request: handle_webhook(bot, dp, config.tg_bot.token, request)
            )

            web.run_app(
                app=app,
                host="0.0.0.0",
                port=8443
            )
        else:
            # Use long polling
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
