import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.config import get_settings
from app.handlers.admin import router as admin_router
from app.handlers.booking import router as booking_router
from app.handlers.common import router as common_router


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


async def create_dispatcher() -> tuple[Bot, Dispatcher]:
    settings = get_settings()
    bot = Bot(token=settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(common_router)
    dp.include_router(booking_router)
    dp.include_router(admin_router)
    return bot, dp
