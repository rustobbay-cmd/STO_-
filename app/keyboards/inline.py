from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


SERVICES = {
    "alignment": {"title": "Развал-схождение", "duration": 1},
    "suspension": {"title": "Ремонт ходовой", "duration": 2},
}


def services_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=data["title"], callback_data=f"svc:{key}")]
            for key, data in SERVICES.items()
        ]
    )


def dates_keyboard(dates: list[str]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=date, callback_data=f"date:{date}")] for date in dates]
    )


def times_keyboard(times: list[str]) -> InlineKeyboardMarkup:
    rows = []
    row = []
    for time_value in times:
        row.append(InlineKeyboardButton(text=time_value, callback_data=f"time:{time_value}"))
        if len(row) == 3:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    return InlineKeyboardMarkup(inline_keyboard=rows)


def user_order_keyboard(order_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="❌ Отменить", callback_data=f"delete:{order_id}")]]
    )


def admin_order_keyboard(order_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="➕ Продлить", callback_data=f"extend:{order_id}"),
            InlineKeyboardButton(text="✅ Завершить", callback_data=f"done:{order_id}"),
        ]]
    )
