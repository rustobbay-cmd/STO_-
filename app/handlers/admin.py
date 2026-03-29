from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from app.config import get_settings
from app.db.sqlite import Database
from app.keyboards.inline import admin_order_keyboard

router = Router()
settings = get_settings()
db = Database(str(settings.database_file))


def _is_admin(user_id: int) -> bool:
    return user_id == settings.admin_id


@router.message(F.text == "📋 План работ (Админ)")
async def admin_panel(message: Message) -> None:
    if not _is_admin(message.from_user.id):
        return

    orders = await db.list_all_orders()
    if not orders:
        await message.answer("План пуст.")
        return

    for order in orders:
        text = (
            f"🕒 {order.name} — {order.date} {order.time}\n"
            f"🛠 {order.service}\n"
            f"🚗 {order.car} ({order.duration} ч.)\n"
            f"📞 {order.phone}"
        )
        if order.service == "Ремонт ходовой":
            await message.answer(text, reply_markup=admin_order_keyboard(order.id))
        else:
            await message.answer(text)


@router.callback_query(F.data.startswith("extend:"))
async def extend_order(callback: CallbackQuery) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Недостаточно прав", show_alert=True)
        return
    order_id = int(callback.data.split(":", 1)[1])
    await db.extend_order(order_id, hours=1)
    await callback.answer("Время продлено")
    await callback.message.edit_text(callback.message.text + "\n⚠️ Продлено на 1 час")


@router.callback_query(F.data.startswith("done:"))
async def complete_order(callback: CallbackQuery) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Недостаточно прав", show_alert=True)
        return
    order_id = int(callback.data.split(":", 1)[1])
    await db.delete_order(order_id)
    await callback.message.edit_text("✅ Работа завершена.")
    await callback.answer()
