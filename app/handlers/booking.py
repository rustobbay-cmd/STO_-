from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.config import get_settings
from app.db.sqlite import Database
from app.keyboards.inline import SERVICES, dates_keyboard, services_keyboard, times_keyboard, user_order_keyboard
from app.keyboards.reply import contact_keyboard, main_keyboard
from app.services.scheduler import generate_date_choices
from app.states import BookingState

router = Router()
settings = get_settings()
db = Database(str(settings.database_file))


@router.message(F.text == "🚗 Записаться")
async def start_booking(message: Message, state: FSMContext) -> None:
    await message.answer("Какая услуга вас интересует?", reply_markup=services_keyboard())
    await state.set_state(BookingState.choosing_service)


@router.callback_query(F.data.startswith("svc:"))
async def service_chosen(callback: CallbackQuery, state: FSMContext) -> None:
    service_key = callback.data.split(":", 1)[1]
    service = SERVICES[service_key]
    await state.update_data(service=service["title"], duration=service["duration"], service_key=service_key)

    if service_key == "alignment":
        await state.update_data(car="Любая", issue="Плановый развал-схождение")
        await _show_dates(callback.message, state)
    else:
        await callback.message.edit_text("Напишите марку и модель авто:")
        await state.set_state(BookingState.asking_car)

    await callback.answer()


@router.message(BookingState.asking_car)
async def ask_issue(message: Message, state: FSMContext) -> None:
    await state.update_data(car=message.text.strip())
    await message.answer("Что именно беспокоит по ходовой?")
    await state.set_state(BookingState.asking_issue)


@router.message(BookingState.asking_issue)
async def issue_received(message: Message, state: FSMContext) -> None:
    await state.update_data(issue=message.text.strip())
    await _show_dates(message, state)


async def _show_dates(event_message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    valid_dates: list[str] = []
    for date_str in generate_date_choices(settings.booking_days_ahead):
        if await db.has_free_slots(date_str, data["duration"], settings.work_start_hour, settings.work_end_hour):
            valid_dates.append(date_str)

    if not valid_dates:
        await event_message.answer("Извините, на ближайшие дни свободных мест нет.")
        await state.clear()
        return

    await event_message.answer("Выберите дату:", reply_markup=dates_keyboard(valid_dates))
    await state.set_state(BookingState.choosing_date)


@router.callback_query(F.data.startswith("date:"))
async def date_chosen(callback: CallbackQuery, state: FSMContext) -> None:
    date_str = callback.data.split(":", 1)[1]
    await state.update_data(date=date_str)
    data = await state.get_data()

    available_times = await db.available_times(
        date_str,
        data["duration"],
        settings.work_start_hour,
        settings.work_end_hour,
    )
    if not available_times:
        await callback.message.edit_text("На выбранную дату свободного времени больше нет.")
        await state.clear()
        await callback.answer()
        return

    await callback.message.edit_text(
        f"Свободное время на {date_str}:",
        reply_markup=times_keyboard(available_times),
    )
    await state.set_state(BookingState.choosing_time)
    await callback.answer()


@router.callback_query(F.data.startswith("time:"))
async def time_chosen(callback: CallbackQuery, state: FSMContext) -> None:
    time_value = callback.data.split(":", 1)[1]
    await state.update_data(time=time_value)
    await callback.message.answer("Оставьте контакт для подтверждения:", reply_markup=contact_keyboard())
    await state.set_state(BookingState.waiting_phone)
    await callback.answer()


@router.message(BookingState.waiting_phone, F.contact)
async def finish_booking(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await db.add_order(
        user_id=message.from_user.id,
        name=message.from_user.full_name,
        phone=message.contact.phone_number,
        car=data["car"],
        issue=data["issue"],
        service=data["service"],
        date=data["date"],
        time=data["time"],
        duration=data["duration"],
    )
    await message.answer(
        f"✅ Записано!\n{data['service']} — {data['date']} в {data['time']}",
        reply_markup=main_keyboard(message.from_user.id == settings.admin_id),
    )
    await message.bot.send_message(
        settings.admin_id,
        (
            "⚡️ Новая запись\n"
            f"Услуга: {data['service']}\n"
            f"Дата: {data['date']}\n"
            f"Время: {data['time']}\n"
            f"Авто: {data['car']}\n"
            f"Клиент: {message.from_user.full_name}\n"
            f"Телефон: {message.contact.phone_number}"
        ),
    )
    await state.clear()


@router.message(F.text == "📅 Мои записи")
async def my_orders(message: Message) -> None:
    orders = await db.list_user_orders(message.from_user.id)
    if not orders:
        await message.answer("У вас нет активных записей.")
        return

    for order in orders:
        await message.answer(
            f"📅 {order.date} в {order.time} — {order.service}",
            reply_markup=user_order_keyboard(order.id),
        )


@router.callback_query(F.data.startswith("delete:"))
async def delete_order(callback: CallbackQuery) -> None:
    order_id = int(callback.data.split(":", 1)[1])
    await db.delete_order(order_id)
    await callback.message.edit_text("❌ Запись отменена.")
    await callback.answer()
