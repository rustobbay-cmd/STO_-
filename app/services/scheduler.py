from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from app.config import get_settings


settings = get_settings()
booking_timezone = ZoneInfo(settings.timezone)


def generate_date_choices(days_ahead: int) -> list[str]:
    now = datetime.now(booking_timezone)
    return [(now + timedelta(days=offset)).strftime("%d.%m") for offset in range(days_ahead)]


def generate_time_slots(start_hour: int, end_hour: int) -> list[str]:
    return [f"{hour}:00" for hour in range(start_hour, end_hour)]
