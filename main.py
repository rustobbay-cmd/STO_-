import asyncio

from app.bot import create_dispatcher, setup_logging
from app.config import get_settings
from app.db.sqlite import Database


async def main() -> None:
    setup_logging()
    settings = get_settings()
    db = Database(str(settings.database_file))
    await db.init()

    bot, dp = await create_dispatcher()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
