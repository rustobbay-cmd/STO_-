from aiogram.fsm.state import State, StatesGroup


class BookingState(StatesGroup):
    choosing_service = State()
    asking_car = State()
    asking_issue = State()
    choosing_date = State()
    choosing_time = State()
    waiting_phone = State()
