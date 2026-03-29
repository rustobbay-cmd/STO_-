from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.config import get_settings
from app.keyboards.reply import main_keyboard

router = Router()
settings = get_settings()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        "СТО Гараж приветствует вас! 🛠\nВыберите действие:",
        reply_markup=main_keyboard(message.from_user.id == settings.admin_id),
    )


@router.message(F.text == "Отмена")
async def cancel_action(message: Message) -> None:
    await message.answer("Действие отменено.", reply_markup=main_keyboard(message.from_user.id == settings.admin_id))
