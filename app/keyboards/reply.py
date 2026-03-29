from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_keyboard(is_admin: bool) -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="🚗 Записаться")],
        [KeyboardButton(text="📅 Мои записи")],
    ]
    if is_admin:
        keyboard.append([KeyboardButton(text="📋 План работ (Админ)")])

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def contact_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Отправить контакт", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
